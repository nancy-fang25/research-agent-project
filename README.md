# Multi-step Research Agent

> **A structured AI system for multi-step document analysis with planning, retrieval, reasoning, and report generation.**


## Overview

This project implements a **multi-step research agent** that can analyze technical documents, perform semantic retrieval (RAG), and generate structured reports.

Unlike standard LLM systems, it follows a **plan → execute → synthesize** workflow and exposes the entire pipeline via a **FastAPI service**.


## Key Features

- Semantic Retrieval (RAG) — chunk-level embedding search
- Task Planning — LLM-based plan generation
- Multi-step Reasoning — tool-driven execution pipeline
- Evaluation System — keyword vs semantic comparison
- Persistent Vector Store — precomputed embeddings
- API Service — FastAPI-based interface
- Structured Outputs — JSON + Markdown report


## System Flow

```text
User Query
    ↓
FastAPI (/query)
    ↓
Planner (LLM)
    ↓
Agent Execution
    ↓
Tools
  ├── search_docs
  ├── summarize_docs
  ├── compare_docs
  └── generate_report
    ↓
Final Report + Execution Trace
```


## Project Structure

```text
research-agent/
├── app/
│   ├── api.py
│   ├── agent.py
│   ├── planner.py
│   ├── tools.py
│   ├── retriever.py
│   └── ...
├── data/
│   ├── sample_docs/
│   └── eval_queries.json
├── demo/
│   ├── report_example.md
│   └── result_example.json
├── outputs/
│   ├── evaluation_report.md
│   └── evaluation_results.json
├── vector_store/   (ignored)
├── PROJECT_SPEC.md
├── README.md
└── requirements.txt
```


## Quick Start

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Run CLI version**
```bash
python -m app.main
```

**3. Run API service**
```bash
uvicorn app.api:app --reload
```

Open the API docs at: `http://127.0.0.1:8000/docs`


## API Usage

**Endpoint:** `POST /query`

**Request Example**
```json
{
  "query": "Compare retrieval and fine-tuning methods",
  "search_method": "vector"
}
```

**Response (simplified)**
```json
{
  "planner_plan": ["search", "summarize", "compare", "report"],
  "result": {
    "search_results": [...],
    "summaries": {...},
    "comparison": "...",
    "report": "..."
  }
}
```


## Evaluation

The system includes a lightweight evaluation framework:
- Top-1 / Top-k retrieval accuracy
- Keyword vs semantic retrieval comparison
- Benchmark queries (`eval_queries.json`)

Detailed results are available in `outputs/evaluation_report.md`.


## Demo Output

**Example Report:** `demo/report_example.md`  
**Example JSON Output:** `demo/result_example.json`


## Tech Stack

- Python
- Sentence Transformers (`all-MiniLM-L6-v2`)
- NumPy
- FastAPI
- Uvicorn


## Limitations

- Small-scale dataset
- No ANN index (brute-force similarity)
- No long-term memory
- Not production deployed


## Future Work

- Hybrid search (BM25 + embeddings)
- Reranker (cross-encoder)
- FAISS / vector database
- Multi-agent architecture
- UI (Streamlit / Web)


## System Design

See: `PROJECT_SPEC.md`


## Key Takeaway

> **This is not a chatbot.**  
> It is a structured, tool-driven, multi-step AI system with planning, retrieval, and evaluation.