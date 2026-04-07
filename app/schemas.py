from typing import List, Dict, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class SearchResult:
    doc_name: str
    score: float
    score_type: str
    retrieval_method: str
    matched_terms: List[str] = field(default_factory=list)
    chunk_id: Optional[int] = None
    chunk_text: Optional[str] = None


@dataclass
class Summary:
    title: str
    abstract_summary: str
    method_summary: str
    results_summary: str
    conclusion_summary: str


@dataclass
class Comparison:
    doc1_title: str
    doc2_title: str
    abstract_comparison: str
    method_comparison: str
    results_comparison: str
    conclusion_comparison: str


@dataclass
class ErrorLog:
    step: str
    message: str


@dataclass
class PlannerOutput:
    plan: List[str]
    rationale: str


@dataclass
class TraceEntry:
    step: str
    status: str
    detail: str


@dataclass
class AgentState:
    query: str
    plan: List[str]
    search_results: List[SearchResult]
    summaries: Dict[str, Summary]
    comparison: Optional[Comparison]
    report: Optional[str]
    errors: List[ErrorLog]
    execution_trace: List[TraceEntry]

    def to_dict(self):
        return asdict(self)