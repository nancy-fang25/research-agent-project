from pathlib import Path
from typing import Literal, Optional

from app.api import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.utils import load_sample_docs
from app.planner import create_plan
from app.agent import run_agent


app = FastAPI(
    title="Research Agent API",
    description="Minimal FastAPI service for the multi-step research agent",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    query: str = Field(..., description="User query for document analysis")
    search_method: Literal["vector", "keyword"] = Field(
        default="vector",
        description="Retrieval method"
    )
    model: str = Field(default="llama3", description="Planner model name")
    data_dir: str = Field(default="data/sample_docs", description="Directory containing sample documents")


class QueryResponse(BaseModel):
    query: str
    search_method: str
    planner_plan: list[str]
    planner_rationale: str
    result: dict


@app.get("/")
def root():
    return {
        "message": "Research Agent API is running",
        "endpoints": {
            "health": "/health",
            "query": "/query"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def run_query(request: QueryRequest):
    data_folder = Path(request.data_dir)

    try:
        docs = load_sample_docs(str(data_folder))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load documents: {e}")

    if not docs:
        raise HTTPException(status_code=400, detail="No documents found in the specified data directory.")

    try:
        planner_output = create_plan(request.query, model=request.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Planner failed: {e}")

    try:
        state = run_agent(
            query=request.query,
            docs=docs,
            plan=planner_output.plan,
            search_method=request.search_method,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {e}")

    return QueryResponse(
        query=request.query,
        search_method=request.search_method,
        planner_plan=planner_output.plan,
        planner_rationale=planner_output.rationale,
        result=state.to_dict(),
    )