import json
from pathlib import Path

from utils import load_sample_docs
from planner import create_plan
from agent import run_agent


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

    plan = create_plan(query)
    state = run_agent(query=query, docs=docs, plan=plan)

    with open(output_folder / "report.md", "w", encoding="utf-8") as f:
        f.write(state.report or "")

    with open(output_folder / "result.json", "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2)

    print("Run completed.")
    print(f"Plan: {state.plan}")
    print("Saved report to outputs/report.md")
    print("Saved result to outputs/result.json")

    if state.errors:
        print("Errors:")
        for err in state.errors:
            print(f"- Step: {err.step} | Message: {err.message}")


if __name__ == "__main__":
    main()