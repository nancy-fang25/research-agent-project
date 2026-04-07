import json
import argparse
import logging
from pathlib import Path

from utils import load_sample_docs
from planner import create_plan
from agent import run_agent


def setup_logging(log_level: str) -> None:
    """
    Configure root logger.
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Multi-step Research Agent for Technical Document Analysis"
    )
    parser.add_argument(
        "--query",
        type=str,
        required=False,
        help="User query for document analysis"
    )  
    parser.add_argument(
        "--model",
        type=str,
        default="llama3",
        help="Ollama model name for planner (default: llama3)",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data/sample_docs",
        help="Directory containing sample documents",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Directory for generated outputs",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging level: DEBUG, INFO, WARNING, ERROR",
    )
    parser.add_argument(
        "--search-method",
        type=str,
        default="vector",
        choices=["vector", "keyword"],
        help="Retrieval method: vector (default) or keyword",
    )    
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    data_folder = Path(args.data_dir)
    output_folder = Path(args.output_dir)
    output_folder.mkdir(parents=True, exist_ok=True)

    if args.query:
        query = args.query
    else:
        query = input("Enter your query: ").strip()

    logger.info("[Main] Loading documents from %s", data_folder)

    try:
        docs = load_sample_docs(str(data_folder))
    except Exception as e:
        logger.exception("[Main] Error loading documents: %s", e)
        return

    logger.info("[Main] Loaded %d document(s)", len(docs))

    planner_output = create_plan(query, model=args.model)
    logger.info("[Planner] Generated plan: %s", planner_output.plan)
    logger.info("[Planner] Rationale: %s", planner_output.rationale)

    state = run_agent(
        query=query,
        docs=docs,
        plan=planner_output.plan,
        search_method=args.search_method,
    )

    result = state.to_dict()
    result["planner_rationale"] = planner_output.rationale

    with open(output_folder / "report.md", "w", encoding="utf-8") as f:
        f.write(state.report or "")

    with open(output_folder / "result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    logger.info("[Main] Saved report to %s", output_folder / "report.md")
    logger.info("[Main] Saved result to %s", output_folder / "result.json")

    if state.errors:
        logger.warning("[Main] Agent finished with %d error(s)", len(state.errors))
        for err in state.errors:
            logger.warning("[Error] Step: %s | Message: %s", err.step, err.message)
    else:
        logger.info("[Main] Agent finished without errors")


if __name__ == "__main__":
    main()