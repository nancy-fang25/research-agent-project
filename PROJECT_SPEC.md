# Multi-step Research Agent for Technical Document Analysis

> **A structured AI system for multi-step document analysis with planning, retrieval, reasoning, and report generation.**


## Purpose

This document describes the system design, architecture, and key decisions behind the research agent.


## Overview

This project implements a **multi-step AI research agent** that can analyze technical documents, perform semantic retrieval, and generate structured reports.

Unlike standard LLM systems, this agent follows a **plan → execute → synthesize** workflow and exposes the pipeline through a **FastAPI service**.


## Problem Statement

Traditional LLM-based systems:

- Answer in a single pass  
- Lack grounding in source documents  
- Provide limited reasoning transparency  

This project addresses these limitations by:

- Performing **chunk-level semantic retrieval**
- Using **explicit task planning**
- Executing **multi-step workflows**
- Returning **structured outputs with evidence**


## Use Cases

The system is designed for:

- Research paper analysis  
- Technical documentation understanding  
- Knowledge synthesis  
- Cross-document comparison  

### Example Queries

- "Summarize the key contributions of this paper"
- "Compare retrieval and fine-tuning methods"
- "Generate a technical report from these documents"


## System Architecture

### High-Level Flow

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

### Execution Pipeline

```text
Query
  ↓
Plan Generation
  ↓
Step 1: Retrieval (semantic chunk search)
  ↓
Step 2: Summarization
  ↓
Step 3: Comparison
  ↓
Step 4: Report Generation
  ↓
Final Output + Execution Trace
```


## Design Decisions

- Why chunk-level retrieval instead of document-level
- Why semantic search over keyword search
- Why separate indexing and query phases
- Trade-offs between simplicity and scalability


## Inputs and Outputs

### Inputs

- Technical documents (TXT / Markdown / PDF)
- User query (provided via CLI or API)
- Retrieval method (`vector` or `keyword`)

### Outputs

The system returns:

- Task plan and rationale  
- Retrieved evidence (chunk-level)  
- Per-document summaries  
- Cross-document comparison  
- Final structured report (Markdown)  
- Execution trace and error logs  


## Core Capabilities

- Tool calling  
- Multi-step reasoning  
- Task planning  
- Structured output  
- Error handling  


## Retrieval (RAG)

- Chunk-level semantic search
- Cosine similarity ranking
- Evidence-backed responses
- Reduced hallucination


## Evaluation

- Top-1 / Top-k retrieval accuracy
- Keyword vs semantic comparison
- Benchmark queries (`eval_queries.json`)


## Persistence

- Precomputed embeddings
- Stored as:
  - `embeddings.npy`    
  - `chunks.json`
- Separates indexing and query phases


## API Service

- FastAPI-based backend
- `/query` endpoint for full pipeline
- `/health` for monitoring
- Auto-generated docs at `/docs`


## Design Highlights

- Modular architecture (planner / agent / tools / retrieval)
- Clear separation of indexing vs querying
- Execution trace for transparency
- Structured JSON + Markdown outputs


## Limitations

- Small-scale dataset
- No ANN index (brute-force similarity)
- No long-term memory
- Not production deployed


## Future Improvements

- Hybrid search (BM25 + embeddings)
- Reranking (cross-encoder)
- FAISS / vector database
- Multi-agent orchestration
- UI / frontend integration


## Summary

This project demonstrates a **complete AI system pipeline**:

- Retrieval (RAG)  
- Planning  
- Multi-step execution  
- Evaluation  
- Persistence  
- API service  

It bridges the gap between:
> **LLM demos → production-style AI systems with structured pipelines and evaluation**


## Key Takeaway

**This is not a chatbot.  
It is a structured, tool-driven, multi-step AI system with explicit planning, retrieval, and evaluation.**