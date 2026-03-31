def create_plan(query: str) -> list[str]:
    """
    Create a simple rule-based execution plan from the user query.
    """
    query_lower = query.lower()
    plan = []

    plan.append("search")

    if "summarize" in query_lower or "summary" in query_lower:
        plan.append("summarize")
    else:
        plan.append("summarize")

    if "compare" in query_lower or "difference" in query_lower:
        plan.append("compare")

    plan.append("report")

    return plan