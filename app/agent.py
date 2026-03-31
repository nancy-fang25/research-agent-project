from tools import search_docs, summarize_docs, compare_docs, generate_report


def run_agent(query: str, docs: dict, plan: list[str]) -> dict:
    """
    Execute the tool pipeline according to the given plan.

    Returns:
        dict containing intermediate state and final outputs
    """
    state = {
        "query": query,
        "plan": plan,
        "search_results": [],
        "summaries": {},
        "comparison": None,
        "report": None,
        "errors": [],
    }

    for step in plan:
        try:
            if step == "search":
                state["search_results"] = search_docs(query, docs)

            elif step == "summarize":
                summaries = {}
                for doc_name, doc_text in docs.items():
                    try:
                        summaries[doc_name] = summarize_docs(doc_text)
                    except Exception as e:
                        summaries[doc_name] = {
                            "title": doc_name,
                            "abstract_summary": f"Error: {e}",
                            "method_summary": "N/A",
                            "results_summary": "N/A",
                            "conclusion_summary": "N/A",
                        }
                state["summaries"] = summaries

            elif step == "compare":
                if len(state["search_results"]) >= 2:
                    doc1_name = state["search_results"][0]["doc_name"]
                    doc2_name = state["search_results"][1]["doc_name"]
                    state["comparison"] = compare_docs(docs[doc1_name], docs[doc2_name])

            elif step == "report":
                state["report"] = generate_report(
                    query=state["query"],
                    search_results=state["search_results"],
                    summaries=state["summaries"],
                    comparison=state["comparison"],
                )

        except Exception as e:
            state["errors"].append({
                "step": step,
                "message": str(e),
            })

    return state