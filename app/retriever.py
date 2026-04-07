from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class RetrievedDoc:
    doc_name: str
    score: float
    matched_terms: List[str]


class DocumentRetriever:
    """
    Minimal semantic retriever for document-level search using
    sentence-transformers + FAISS.

    Flow:
    docs -> embeddings -> FAISS index
    query -> embedding -> top-k document retrieval
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

        self.doc_names: List[str] = []
        self.doc_texts: List[str] = []
        self.doc_embeddings: np.ndarray | None = None
        self.index: faiss.Index | None = None

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        """
        Normalize vectors so inner product == cosine similarity.
        """
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms = np.clip(norms, a_min=1e-12, a_max=None)
        return vectors / norms

    def build_index(self, docs: Dict[str, str]) -> None:
        """
        Build FAISS index from input documents.

        Args:
            docs: {doc_name: doc_text}
        """
        if not docs:
            raise ValueError("No documents provided to build the retriever index.")

        self.doc_names = list(docs.keys())
        self.doc_texts = [docs[name] for name in self.doc_names]

        embeddings = self.model.encode(
            self.doc_texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")

        embeddings = self._normalize(embeddings)

        self.doc_embeddings = embeddings
        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)
        self.index = index

    def search(self, query: str, top_k: int = 3) -> List[RetrievedDoc]:
        """
        Search the FAISS index with a query.

        Args:
            query: user query
            top_k: number of documents to return

        Returns:
            list of RetrievedDoc
        """
        if self.index is None:
            raise ValueError("Retriever index has not been built yet.")

        if not query.strip():
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")

        query_embedding = self._normalize(query_embedding)

        top_k = min(top_k, len(self.doc_names))
        scores, indices = self.index.search(query_embedding, top_k)

        results: List[RetrievedDoc] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            results.append(
                RetrievedDoc(
                    doc_name=self.doc_names[idx],
                    score=float(score),
                    matched_terms=[],
                )
            )

        return results