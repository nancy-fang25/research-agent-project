import re
from collections import Counter

STOPWORDS = {
    "the", "a", "an", "and", "or", "in", "on", "of", "to", "for",
    "with", "by", "these", "this", "that", "is", "are", "be", "as",
    "at", "from", "into", "documents"
}


def tokenize(text: str) -> list[str]:
    """Simple tokenizer: lowercase + keep words only."""
    return re.findall(r"\b[a-zA-Z][a-zA-Z0-9\-]*\b", text.lower())


def split_sections(doc_text: str) -> dict:
    """
    Parse a structured sample doc into sections.

    Expected format:
    Title: ...
    Abstract:
    ...
    Method:
    ...
    Results:
    ...
    Conclusion:
    ...
    """
    sections = {}
    current_section = None
    buffer = []

    for line in doc_text.splitlines():
        stripped = line.strip()

        if stripped.startswith("Title:"):
            sections["Title"] = stripped.replace("Title:", "", 1).strip()
            continue

        if stripped in {"Abstract:", "Method:", "Results:", "Conclusion:"}:
            if current_section and buffer:
                sections[current_section] = "\n".join(buffer).strip()
            current_section = stripped[:-1]
            buffer = []
            continue

        if current_section:
            buffer.append(line)

    if current_section and buffer:
        sections[current_section] = "\n".join(buffer).strip()

    return sections


def search_docs(query: str, docs: dict) -> list[dict]:
    """
    Search documents by simple keyword overlap, with stopword filtering.

    Args:
        query: user query
        docs: {doc_name: doc_text}

    Returns:
        ranked list of matches
    """
    query_tokens = {t for t in tokenize(query) if t not in STOPWORDS}
    results = []

    for doc_name, doc_text in docs.items():
        doc_tokens = tokenize(doc_text)
        doc_counter = Counter(doc_tokens)

        score = sum(doc_counter[token] for token in query_tokens)

        if score > 0:
            results.append({
                "doc_name": doc_name,
                "score": score,
                "matched_terms": sorted([t for t in query_tokens if t in doc_counter]),
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def summarize_docs(doc_text: str) -> dict:
    """
    Return a structured summary from the sample doc sections.
    """
    sections = split_sections(doc_text)

    return {
        "title": sections.get("Title", "Unknown Title"),
        "abstract_summary": sections.get("Abstract", "No abstract found."),
        "method_summary": sections.get("Method", "No method found."),
        "results_summary": sections.get("Results", "No results found."),
        "conclusion_summary": sections.get("Conclusion", "No conclusion found."),
    }


def compare_docs(doc1_text: str, doc2_text: str) -> dict:
    """
    Compare two docs by section content.
    """
    s1 = summarize_docs(doc1_text)
    s2 = summarize_docs(doc2_text)

    return {
        "doc1_title": s1["title"],
        "doc2_title": s2["title"],
        "abstract_comparison": (
            f"Doc 1 focuses on: {s1['abstract_summary']} "
            f"Doc 2 focuses on: {s2['abstract_summary']}"
        ),
        "method_comparison": (
            f"Doc 1 method: {s1['method_summary']} "
            f"Doc 2 method: {s2['method_summary']}"
        ),
        "results_comparison": (
            f"Doc 1 results: {s1['results_summary']} "
            f"Doc 2 results: {s2['results_summary']}"
        ),
        "conclusion_comparison": (
            f"Doc 1 concludes: {s1['conclusion_summary']} "
            f"Doc 2 concludes: {s2['conclusion_summary']}"
        ),
    }


def generate_report(
    query: str,
    search_results: list,
    summaries: dict,
    comparison: dict | None = None
) -> str:
    """
    Generate a markdown report.

    Document summaries are shown in ranked search order first,
    then any remaining documents are appended.
    """
    lines = []
    lines.append("# Technical Document Analysis Report")
    lines.append("")
    lines.append("## User Query")
    lines.append(query)
    lines.append("")

    lines.append("## Search Results")
    if not search_results:
        lines.append("No relevant documents found.")
    else:
        for item in search_results:
            lines.append(
                f"- **{item['doc_name']}** | score={item['score']} | matched_terms={', '.join(item['matched_terms'])}"
            )
    lines.append("")

    lines.append("## Document Summaries")

    # First: summaries in ranked search order
    added_docs = set()
    for item in search_results:
        doc_name = item["doc_name"]
        if doc_name in summaries:
            summary = summaries[doc_name]
            lines.append(f"### {doc_name}")
            lines.append(f"- **Title:** {summary['title']}")
            lines.append(f"- **Abstract:** {summary['abstract_summary']}")
            lines.append(f"- **Method:** {summary['method_summary']}")
            lines.append(f"- **Results:** {summary['results_summary']}")
            lines.append(f"- **Conclusion:** {summary['conclusion_summary']}")
            lines.append("")
            added_docs.add(doc_name)

    # Then: any remaining docs not in search results
    for doc_name, summary in summaries.items():
        if doc_name not in added_docs:
            lines.append(f"### {doc_name}")
            lines.append(f"- **Title:** {summary['title']}")
            lines.append(f"- **Abstract:** {summary['abstract_summary']}")
            lines.append(f"- **Method:** {summary['method_summary']}")
            lines.append(f"- **Results:** {summary['results_summary']}")
            lines.append(f"- **Conclusion:** {summary['conclusion_summary']}")
            lines.append("")

    if comparison:
        lines.append("## Document Comparison")
        lines.append(f"- **Doc 1:** {comparison['doc1_title']}")
        lines.append(f"- **Doc 2:** {comparison['doc2_title']}")
        lines.append(f"- **Abstract:** {comparison['abstract_comparison']}")
        lines.append(f"- **Method:** {comparison['method_comparison']}")
        lines.append(f"- **Results:** {comparison['results_comparison']}")
        lines.append(f"- **Conclusion:** {comparison['conclusion_comparison']}")
        lines.append("")

    return "\n".join(lines)