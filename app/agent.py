from tools import search_docs, summarize_docs, compare_docs, generate_report
from schemas import AgentState, SearchResult, Summary, Comparison, ErrorLog


def run_agent(query: str, docs: dict, plan: list[str]) -> AgentState:
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
    )

    for step in plan:
        try:
            if step == "search":
                results = search_docs(query, docs)
                state.search_results = [SearchResult(**r) for r in results]

            elif step == "summarize":
                summaries = {}
                for doc_name, doc_text in docs.items():
                    try:
                        s = summarize_docs(doc_text)
                        summaries[doc_name] = Summary(**s)
                    except Exception as e:
                        summaries[doc_name] = Summary(
                            title=doc_name,
                            abstract_summary=f"Error: {e}",
                            method_summary="N/A",
                            results_summary="N/A",
                            conclusion_summary="N/A",
                        )
                state.summaries = summaries

            elif step == "compare":
                if len(state.search_results) >= 2:
                    doc1_name = state.search_results[0].doc_name
                    doc2_name = state.search_results[1].doc_name

                    comp = compare_docs(docs[doc1_name], docs[doc2_name])
                    state.comparison = Comparison(**comp)

            elif step == "report":
                search_results_for_report = [
                    {
                        "doc_name": r.doc_name,
                        "score": r.score,
                        "matched_terms": r.matched_terms,
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

        except Exception as e:
            state.errors.append(ErrorLog(
                step=step,
                message=str(e),
            ))

    return state