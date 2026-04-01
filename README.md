# Multi-step Research Agent for Technical Document Analysis

A multi-step AI agent for technical document analysis with tool calling, structured outputs, and local LLM-based planning via Ollama.

---

## Overview

This project implements a modular AI agent that processes technical documents through a sequence of steps including retrieval, summarization, comparison, and report generation.

Unlike a static pipeline, the system dynamically generates an execution plan from a natural language query using a local large language model (LLM), enabling flexible and adaptive workflows.

---

## Key Features

### Modular Tool Pipeline
Implements a structured workflow:
```text
search → summarize → compare → report
```

Each step is encapsulated as a tool, enabling clear separation of concerns.

---

### Plan-Driven Agent Architecture

Transforms a fixed pipeline into a dynamic agent:

- Generates execution plans based on user queries
- Executes steps sequentially according to the plan
- Supports flexible workflows depending on task intent

---

### LLM-based Planning (Local via Ollama)
- Uses a local LLM (e.g. llama3) to generate plans
- Understands query intent (e.g. comparison vs summarization)
- Includes fallback rule-based planner for robustness

---

### Structured State Management

Uses dataclass-based schemas to manage:
- search results
- summaries
- comparisons
- errors
- execution trace

Ensures consistent and debuggable outputs.

---

### Execution Trace & Logging
- Tracks each step of execution
- Records success, failure, or skipped steps
- Provides transparency and debugging capability

Example trace:
```json
{
  "step": "compare",
  "status": "success",
  "detail": "Compared top 2 documents"
}
```

---

### CLI and Interactive Input

The agent supports both CLI-based input and interactive input.

#### Option 1: CLI input (recommended)

```bash
python app/main.py --query "Compare retrieval and fine-tuning methods"
```

#### Option 2: Interactive input
```bash
python app/main.py
```
Then enter your query when prompted:
```text
Enter your query: Compare retrieval and fine-tuning methods
```
This allows the agent to be used both in scripted workflows and interactive scenarios.

---

You can also specify optional parameters:
```bash
--model llama3
--log-level DEBUG
```

---

## Project Structure
```text
research-agent/
├── app/
│   ├── agent.py        # execution engine
│   ├── main.py         # CLI entry point
│   ├── planner.py      # LLM + fallback planner
│   ├── schemas.py      # structured state
│   ├── tools.py        # tool functions
│   └── utils.py        # data loading
├── data/
│   └── sample_docs/    # demo documents
├── demo/               # example outputs
├── tests/
├── requirements.txt
└── README.md
```

---

## System Workflow

### High-level flow
```text
User Query
   ↓
Planner (LLM or fallback)
   ↓
Execution Plan
   ↓
Agent Execution
   ↓
Report + JSON Output
```

---

### Internal agent execution
```text
search → summarize → compare → report
```

---

## Installation
```bash
pip install -r requirements.txt
```

---

## Requirements
- Python 3.10+
- Ollama installed locally
- A local model such as llama3

---

## Usage

### Basic usage (CLI)

```bash
python app/main.py --query "Compare retrieval and fine-tuning methods in these technical documents"
```

---

### Interactive mode
```bash
python app/main.py
```
Then enter your query when prompted.

---

### Debug mode
```bash
python app/main.py --query "Summarize these documents" --log-level DEBUG
```

---

## Output

The system generates:

1. Markdown Report
```text
outputs/report.md
```
Human-readable structured analysis.

---

2. JSON Result
```text
outputs/result.json
```
Contains:
- query
- plan
- search_results
- summaries
- comparison
- report
- errors
- execution_trace
- planner_rationale

---

## Example Capabilities
- Compare technical approaches (e.g. RAG vs fine-tuning)
- Summarize multiple documents
- Generate structured reports
- Track execution for debugging and analysis

---

## Design Principles
- Separation of concerns: tools, planner, and agent are decoupled
- Robustness: fallback planner ensures system always runs
- Observability: execution trace and logging for transparency
- Local-first: uses local LLM (Ollama) instead of external APIs
- Extensibility: easy to add new tools or steps

---

## Notes
- Sample documents are synthetic and safe for public use
- Outputs are generated dynamically and not tracked in Git
- Planner behavior depends on the local LLM model

---

## Resume-ready Summary

Built a multi-step AI agent for technical document analysis with local LLM-based planning, tool calling, structured state management, execution tracing, and markdown/JSON report generation.
