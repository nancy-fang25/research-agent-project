import json
from pathlib import Path
from typing import Any

from utils import load_sample_docs
from tools import search_docs


def load_eval_queries(path: str) -> list[dict[str, Any]]:
    """
    Load evaluation queries from a JSON file.

    Expected format:
    [
      {
        "query": "Which paper discusses AI agents?",
        "expected_docs": ["paper3.txt"]
      },
      ...
    ]
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Evaluation query file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Evaluation query file must contain a list of query records.")

    validated = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Query record at index {i} must be a dictionary.")

        query = item.get("query")
        expected_docs = item.get("expected_docs")

        if not isinstance(query, str) or not query.strip():
            raise ValueError(f"Query record at index {i} is missing a valid 'query' string.")

        if not isinstance(expected_docs, list) or not all(isinstance(x, str) for x in expected_docs):
            raise ValueError(
                f"Query record at index {i} must contain 'expected_docs' as a list of strings."
            )

        validated.append(
            {
                "query": query.strip(),
                "expected_docs": expected_docs,
            }
        )

    return validated


def extract_doc_names(results: list[dict[str, Any]]) -> list[str]:
    """
    Extract retrieved document names in ranked order.
    Duplicate document names are removed while preserving order.
    """
    doc_names = []
    seen = set()

    for item in results:
        doc_name = item.get("doc_name")
        if isinstance(doc_name, str) and doc_name not in seen:
            doc_names.append(doc_name)
            seen.add(doc_name)

    return doc_names


def get_correct_doc_rank(retrieved_docs: list[str], expected_docs: list[str]) -> int | None:
    """
    Return the 1-based rank of the first correct document.
    If no correct document is found, return None.
    """
    for i, doc_name in enumerate(retrieved_docs):
        if doc_name in expected_docs:
            return i + 1
    return None


def format_result_preview(results: list[dict[str, Any]], max_items: int = 3) -> list[str]:
    """
    Build short human-readable previews for top retrieved results.
    Useful for the markdown report.
    """
    previews = []

    for item in results[:max_items]:
        doc_name = item.get("doc_name", "unknown")
        score = item.get("score", "N/A")
        retrieval_method = item.get("retrieval_method", "unknown")
        chunk_id = item.get("chunk_id")

        if retrieval_method == "semantic_chunk":
            previews.append(f"{doc_name} | chunk={chunk_id} | similarity={score}")
        else:
            matched_terms = item.get("matched_terms", [])
            matched_str = ", ".join(matched_terms) if matched_terms else "N/A"
            previews.append(f"{doc_name} | score={score} | matched_terms={matched_str}")

    return previews


def evaluate_method(
    query: str,
    expected_docs: list[str],
    docs: dict[str, str],
    method: str,
    top_k: int = 3,
) -> dict[str, Any]:
    """
    Evaluate one retrieval method on one query.

    Metrics:
    - Top-1 Hit: whether the first retrieved doc is in expected_docs
    - Top-k Hit: whether any of the top-k retrieved docs is in expected_docs
    - Correct Rank: the rank position of the first correct document
    """
    try:
        results = search_docs(query=query, docs=docs, method=method, top_k=top_k)
    except Exception as e:
        return {
            "method": method,
            "retrieved_docs": [],
            "top1_hit": False,
            "topk_hit": False,
            "correct_rank": None,
            "raw_results": [],
            "result_preview": [],
            "error": str(e),
        }

    retrieved_docs = extract_doc_names(results)
    correct_rank = get_correct_doc_rank(retrieved_docs, expected_docs)

    top1_hit = bool(retrieved_docs) and (retrieved_docs[0] in expected_docs)
    topk_hit = any(doc_name in expected_docs for doc_name in retrieved_docs[:top_k])

    return {
        "method": method,
        "retrieved_docs": retrieved_docs,
        "top1_hit": top1_hit,
        "topk_hit": topk_hit,
        "correct_rank": correct_rank,
        "raw_results": results,
        "result_preview": format_result_preview(results, max_items=top_k),
        "error": None,
    }


def run_evaluation(
    docs: dict[str, str],
    eval_queries: list[dict[str, Any]],
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """
    Run evaluation for all queries using both keyword and vector retrieval.
    """
    records = []

    for item in eval_queries:
        query = item["query"]
        expected_docs = item["expected_docs"]

        keyword_result = evaluate_method(
            query=query,
            expected_docs=expected_docs,
            docs=docs,
            method="keyword",
            top_k=top_k,
        )

        vector_result = evaluate_method(
            query=query,
            expected_docs=expected_docs,
            docs=docs,
            method="vector",
            top_k=top_k,
        )

        records.append(
            {
                "query": query,
                "expected_docs": expected_docs,
                "keyword": keyword_result,
                "vector": vector_result,
            }
        )

    return records


def summarize_scores(records: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Aggregate hit statistics and ranking statistics across all evaluation queries.
    """
    total = len(records)

    keyword_top1_hits = sum(1 for r in records if r["keyword"]["top1_hit"])
    keyword_topk_hits = sum(1 for r in records if r["keyword"]["topk_hit"])
    vector_top1_hits = sum(1 for r in records if r["vector"]["top1_hit"])
    vector_topk_hits = sum(1 for r in records if r["vector"]["topk_hit"])

    keyword_errors = sum(1 for r in records if r["keyword"]["error"] is not None)
    vector_errors = sum(1 for r in records if r["vector"]["error"] is not None)

    keyword_ranks = [r["keyword"]["correct_rank"] for r in records if r["keyword"]["correct_rank"] is not None]
    vector_ranks = [r["vector"]["correct_rank"] for r in records if r["vector"]["correct_rank"] is not None]

    avg_keyword_rank = sum(keyword_ranks) / len(keyword_ranks) if keyword_ranks else None
    avg_vector_rank = sum(vector_ranks) / len(vector_ranks) if vector_ranks else None

    return {
        "total_queries": total,
        "keyword_top1_hits": keyword_top1_hits,
        "keyword_topk_hits": keyword_topk_hits,
        "vector_top1_hits": vector_top1_hits,
        "vector_topk_hits": vector_topk_hits,
        "keyword_top1_rate": keyword_top1_hits / total if total else 0.0,
        "keyword_topk_rate": keyword_topk_hits / total if total else 0.0,
        "vector_top1_rate": vector_top1_hits / total if total else 0.0,
        "vector_topk_rate": vector_topk_hits / total if total else 0.0,
        "keyword_errors": keyword_errors,
        "vector_errors": vector_errors,
        "avg_keyword_rank": avg_keyword_rank,
        "avg_vector_rank": avg_vector_rank,
    }


def generate_evaluation_report(
    records: list[dict[str, Any]],
    summary: dict[str, Any],
    top_k: int = 3,
) -> str:
    """
    Generate a markdown evaluation report.
    """
    lines = []
    lines.append("# Retrieval Evaluation Report")
    lines.append("")
    lines.append("## Goal")
    lines.append(
        "This report compares keyword-based retrieval and semantic chunk-level retrieval "
        "on a small benchmark of representative queries."
    )
    lines.append("")
    lines.append("## Metrics")
    lines.append("- **Top-1 Hit**: whether the first retrieved document is correct")
    lines.append(f"- **Top-{top_k} Hit**: whether any of the top-{top_k} retrieved documents is correct")
    lines.append("- **Correct Doc Rank**: the rank position of the first correct document")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total queries: {summary['total_queries']}")
    lines.append(
        f"- Keyword Top-1 Hit Rate: {summary['keyword_top1_hits']}/{summary['total_queries']} "
        f"({summary['keyword_top1_rate']:.2%})"
    )
    lines.append(
        f"- Keyword Top-{top_k} Hit Rate: {summary['keyword_topk_hits']}/{summary['total_queries']} "
        f"({summary['keyword_topk_rate']:.2%})"
    )
    lines.append(
        f"- Vector Top-1 Hit Rate: {summary['vector_top1_hits']}/{summary['total_queries']} "
        f"({summary['vector_top1_rate']:.2%})"
    )
    lines.append(
        f"- Vector Top-{top_k} Hit Rate: {summary['vector_topk_hits']}/{summary['total_queries']} "
        f"({summary['vector_topk_rate']:.2%})"
    )
    lines.append(f"- Keyword Errors: {summary['keyword_errors']}")
    lines.append(f"- Vector Errors: {summary['vector_errors']}")

    if summary["avg_keyword_rank"] is not None:
        lines.append(f"- Avg Keyword Correct Rank: {summary['avg_keyword_rank']:.2f}")
    else:
        lines.append("- Avg Keyword Correct Rank: N/A")

    if summary["avg_vector_rank"] is not None:
        lines.append(f"- Avg Vector Correct Rank: {summary['avg_vector_rank']:.2f}")
    else:
        lines.append("- Avg Vector Correct Rank: N/A")

    lines.append("")

    for i, record in enumerate(records, start=1):
        lines.append(f"## Query {i}")
        lines.append(f"**Query:** {record['query']}")
        lines.append(f"**Expected Docs:** {', '.join(record['expected_docs'])}")
        lines.append("")

        for method_name in ["keyword", "vector"]:
            method_result = record[method_name]
            pretty_name = "Keyword" if method_name == "keyword" else "Vector"

            lines.append(f"### {pretty_name}")
            lines.append(
                f"- Retrieved Docs: "
                f"{', '.join(method_result['retrieved_docs']) if method_result['retrieved_docs'] else 'None'}"
            )
            lines.append(f"- Top-1 Hit: {'Yes' if method_result['top1_hit'] else 'No'}")
            lines.append(f"- Top-{top_k} Hit: {'Yes' if method_result['topk_hit'] else 'No'}")

            rank = method_result.get("correct_rank")
            rank_str = str(rank) if rank is not None else "Not Found"
            lines.append(f"- Correct Doc Rank: {rank_str}")

            if method_result["error"]:
                lines.append(f"- Error: {method_result['error']}")
            else:
                preview_items = method_result.get("result_preview", [])
                if preview_items:
                    lines.append("- Top Results Preview:")
                    for preview in preview_items:
                        lines.append(f"  - {preview}")

            lines.append("")

    lines.append("## Observations")
    lines.append("")
    lines.append(
        "- In this small benchmark, both keyword retrieval and semantic vector retrieval may achieve high hit rates "
        "because the dataset contains only a few short documents."
    )
    lines.append(
        "- The limited corpus size makes retrieval relatively easy, so hit-based metrics alone may not fully reveal "
        "the difference between lexical matching and semantic matching."
    )
    lines.append(
        "- Even when both methods retrieve the correct document, semantic chunk retrieval can still provide better "
        "grounding by returning more focused and query-relevant evidence snippets."
    )
    lines.append(
        "- The added ranking signal helps compare retrieval quality more precisely, since a method may rank the correct "
        "document higher even when both methods achieve the same hit rate."
    )
    lines.append(
        "- A larger benchmark with more documents, stronger paraphrased queries, and more distractor content would "
        "better highlight the advantage of semantic retrieval."
    )
    lines.append(
        "- This evaluation is intended as a lightweight sanity check and comparison baseline rather than a full-scale "
        "retrieval study."
    )

    return "\n".join(lines)


def save_json(data: dict[str, Any], path: Path) -> None:
    """
    Save JSON with UTF-8 encoding and indentation.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main() -> None:
    data_dir = "data/sample_docs"
    eval_query_path = "data/eval_queries.json"
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "evaluation_report.md"
    result_path = output_dir / "evaluation_results.json"

    top_k = 3

    print("[Eval] Loading documents...")
    docs = load_sample_docs(data_dir)
    if not docs:
        raise ValueError("No documents were loaded. Please check data/sample_docs.")

    print("[Eval] Loading evaluation queries...")
    eval_queries = load_eval_queries(eval_query_path)
    if not eval_queries:
        raise ValueError("No evaluation queries found. Please check data/eval_queries.json.")

    print("[Eval] Running evaluation...")
    records = run_evaluation(docs=docs, eval_queries=eval_queries, top_k=top_k)

    print("[Eval] Summarizing results...")
    summary = summarize_scores(records)

    print("[Eval] Generating report...")
    report = generate_evaluation_report(records, summary, top_k=top_k)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    save_json(
        {
            "summary": summary,
            "records": records,
        },
        result_path,
    )

    print(f"[Eval] Saved report to {report_path}")
    print(f"[Eval] Saved results to {result_path}")


if __name__ == "__main__":
    main()