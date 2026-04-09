import logging

from app.tools import search_docs, summarize_docs, compare_docs, generate_report
from app.schemas import AgentState, SearchResult, Summary, Comparison, ErrorLog, TraceEntry


logger = logging.getLogger(__name__)


def run_agent(query: str, docs: dict, plan: list[str], search_method: str = "vector") -> AgentState:
    """
    Execute the tool pipeline according to the given plan.

    Returns:
        AgentState containing intermediate state and final outputs
    """
    state = AgentState(
        query=query,
        plan=plan,
        search_results=[],
        summaries={},
        comparison=None,
        report=None,
        errors=[],
        execution_trace=[],
    )

    logger.info("[Agent] Starting execution")
    logger.info("[Agent] Plan: %s", plan)

    for step in plan:
        try:
            logger.info("[Agent] Running step: %s", step)

            if step == "search":
                results = search_docs(query, docs, method=search_method)
                state.search_results = [SearchResult(**r) for r in results]

                detail = f"Found {len(state.search_results)} relevant document(s)."
                state.execution_trace.append(
                    TraceEntry(step="search", status="success", detail=detail)
                )
                logger.info("[Search] %s", detail)

            elif step == "summarize":
                summaries = {}
                success_count = 0

                for doc_name, doc_text in docs.items():
                    try:
                        s = summarize_docs(doc_text)
                        summaries[doc_name] = Summary(**s)
                        success_count += 1
                    except Exception as e:
                        summaries[doc_name] = Summary(
                            title=doc_name,
                            abstract_summary=f"Error: {e}",
                            method_summary="N/A",
                            results_summary="N/A",
                            conclusion_summary="N/A",
                        )
                        logger.warning("[Summarize] Failed on %s: %s", doc_name, e)

                state.summaries = summaries

                detail = f"Generated summaries for {success_count}/{len(docs)} document(s)."
                state.execution_trace.append(
                    TraceEntry(step="summarize", status="success", detail=detail)
                )
                logger.info("[Summarize] %s", detail)

            elif step == "compare":
                unique_docs = []
                for item in state.search_results:
                    if item.doc_name not in unique_docs:
                        unique_docs.append(item.doc_name)
                    if len(unique_docs) == 2:
                        break

                if len(unique_docs) >= 2:
                    doc1_name, doc2_name = unique_docs[0], unique_docs[1]

                    comp = compare_docs(docs[doc1_name], docs[doc2_name])
                    state.comparison = Comparison(**comp)

                    detail = f"Compared top 2 documents: {doc1_name} vs {doc2_name}."
                    state.execution_trace.append(
                        TraceEntry(step="compare", status="success", detail=detail)
                    )
                    logger.info("[Compare] %s", detail)
                else:
                    detail = "Skipped comparison because fewer than 2 distinct relevant documents were found."
                    state.execution_trace.append(
                        TraceEntry(step="compare", status="skipped", detail=detail)
                    )
                    logger.info("[Compare] %s", detail)

            elif step == "report":
                search_results_for_report = [
                    {
                        "doc_name": r.doc_name,
                        "score": r.score,
                        "score_type": r.score_type,
                        "retrieval_method": r.retrieval_method,
                        "matched_terms": r.matched_terms,
                        "chunk_id": r.chunk_id,
                        "chunk_text": r.chunk_text,
                    }
                    for r in state.search_results
                ]

                summaries_for_report = {
                    doc_name: {
                        "title": s.title,
                        "abstract_summary": s.abstract_summary,
                        "method_summary": s.method_summary,
                        "results_summary": s.results_summary,
                        "conclusion_summary": s.conclusion_summary,
                    }
                    for doc_name, s in state.summaries.items()
                }

                comparison_for_report = None
                if state.comparison is not None:
                    comparison_for_report = {
                        "doc1_title": state.comparison.doc1_title,
                        "doc2_title": state.comparison.doc2_title,
                        "abstract_comparison": state.comparison.abstract_comparison,
                        "method_comparison": state.comparison.method_comparison,
                        "results_comparison": state.comparison.results_comparison,
                        "conclusion_comparison": state.comparison.conclusion_comparison,
                    }

                state.report = generate_report(
                    query=state.query,
                    search_results=search_results_for_report,
                    summaries=summaries_for_report,
                    comparison=comparison_for_report,
                )

                detail = "Generated final markdown report."
                state.execution_trace.append(
                    TraceEntry(step="report", status="success", detail=detail)
                )
                logger.info("[Report] %s", detail)

            else:
                detail = f"Unknown step '{step}' was ignored."
                state.execution_trace.append(
                    TraceEntry(step=step, status="skipped", detail=detail)
                )
                logger.warning("[Agent] %s", detail)

        except Exception as e:
            state.errors.append(ErrorLog(step=step, message=str(e)))
            state.execution_trace.append(
                TraceEntry(step=step, status="error", detail=str(e))
            )
            logger.exception("[Agent] Step failed: %s", step)

    logger.info("[Agent] Execution finished")
    return state