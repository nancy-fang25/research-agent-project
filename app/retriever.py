from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class RetrievedChunk:
    doc_name: str
    chunk_id: int
    chunk_text: str
    score: float
    retrieval_method: str
    score_type: str


class ChunkRetriever:
    """
    Chunk-level semantic retriever using sentence-transformers + numpy similarity.

    Flow:
    docs -> chunks -> embeddings
    query -> embedding -> similarity -> top-k chunks
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        chunk_size: int = 80,
        chunk_overlap: int = 20,
    ) -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.chunks: List[dict] = []
        self.chunk_embeddings: np.ndarray | None = None

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms = np.clip(norms, a_min=1e-12, a_max=None)
        return vectors / norms

    def _split_into_chunks(self, text: str) -> List[str]:
        """
        Split text into overlapping word chunks.
        """
        words = text.split()
        if not words:
            return []

        chunks = []
        step = max(1, self.chunk_size - self.chunk_overlap)

        for start in range(0, len(words), step):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            if not chunk_words:
                continue
            chunks.append(" ".join(chunk_words))
            if end >= len(words):
                break

        return chunks

    def build_index(self, docs: Dict[str, str]) -> None:
        """
        Build chunk-level embedding store.
        """
        if not docs:
            raise ValueError("No documents provided to build the retriever index.")

        all_chunks: List[dict] = []

        for doc_name, doc_text in docs.items():
            chunk_texts = self._split_into_chunks(doc_text)

            for i, chunk_text in enumerate(chunk_texts):
                all_chunks.append(
                    {
                        "doc_name": doc_name,
                        "chunk_id": i,
                        "chunk_text": chunk_text,
                    }
                )

        if not all_chunks:
            raise ValueError("No chunks were created from the input documents.")

        self.chunks = all_chunks

        texts = [c["chunk_text"] for c in all_chunks]
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")

        self.chunk_embeddings = self._normalize(embeddings)

    def search(self, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        """
        Search top-k chunks by cosine similarity.
        """
        if self.chunk_embeddings is None or not self.chunks:
            raise ValueError("Retriever index has not been built yet.")

        if not query.strip():
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")

        query_embedding = self._normalize(query_embedding)

        scores = np.dot(self.chunk_embeddings, query_embedding.T).squeeze()
        top_k = min(top_k, len(self.chunks))
        top_indices = np.argsort(scores)[::-1][:top_k]

        results: List[RetrievedChunk] = []
        for idx in top_indices:
            chunk = self.chunks[int(idx)]
            results.append(
                RetrievedChunk(
                    doc_name=chunk["doc_name"],
                    chunk_id=chunk["chunk_id"],
                    chunk_text=chunk["chunk_text"],
                    score=float(scores[idx]),
                    retrieval_method="semantic_chunk",
                    score_type="cosine_similarity",
                )
            )

        return results