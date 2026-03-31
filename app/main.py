import json
from pathlib import Path

from utils import load_sample_docs
from tools import search_docs, summarize_docs, compare_docs, generate_report


def main():
    data_folder = Path("data/sample_docs")
    output_folder = Path("outputs")
    output_folder.mkdir(parents=True, exist_ok=True)

    query = "Compare retrieval and fine-tuning methods in these technical documents"

    try:
        docs = load_sample_docs(str(data_folder))
    except Exception as e:
        print(f"Error loading documents: {e}")
        return

    search_results = search_docs(query, docs)

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

    comparison = None
    if len(search_results) >= 2:
        doc1_name = search_results[0]["doc_name"]
        doc2_name = search_results[1]["doc_name"]
        comparison = compare_docs(docs[doc1_name], docs[doc2_name])

    report = generate_report(
        query=query,
        search_results=search_results,
        summaries=summaries,
        comparison=comparison,
    )

    result_json = {
        "query": query,
        "search_results": search_results,
        "summaries": summaries,
        "comparison": comparison,
    }

    with open(output_folder / "report.md", "w", encoding="utf-8") as f:
        f.write(report)

    with open(output_folder / "result.json", "w", encoding="utf-8") as f:
        json.dump(result_json, f, indent=2)

    print("Run completed.")
    print("Saved report to outputs/report.md")
    print("Saved result to outputs/result.json")


if __name__ == "__main__":
    main()
