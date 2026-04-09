from pathlib import Path

from utils import load_sample_docs
from retriever import ChunkRetriever


def main() -> None:
    data_dir = "data/sample_docs"
    output_dir = Path("vector_store")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("[Index] Loading documents...")
    docs = load_sample_docs(data_dir)

    if not docs:
        raise ValueError("No documents were loaded. Please check data/sample_docs.")

    print(f"[Index] Loaded {len(docs)} document(s).")

    retriever = ChunkRetriever(
        model_name="all-MiniLM-L6-v2",
        chunk_size=80,
        chunk_overlap=20,
    )

    print("[Index] Building chunk-level vector index...")
    retriever.build_index(docs)

    print(f"[Index] Built index with {len(retriever.chunks)} chunk(s).")

    print(f"[Index] Saving index to {output_dir} ...")
    retriever.save_index(str(output_dir))

    print("[Index] Done.")
    print(f"[Index] Saved embeddings to {output_dir / 'embeddings.npy'}")
    print(f"[Index] Saved chunk metadata to {output_dir / 'chunks.json'}")


if __name__ == "__main__":
    main()