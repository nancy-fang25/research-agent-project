from pathlib import Path


def load_text_file(file_path: str) -> str:
    """Load a single text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read() 


def load_sample_docs(folder_path: str) -> dict:
    """
    Load all .txt documents from a folder.

    Returns:
        dict: {filename: file_content}
    """
    docs = {}
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    for file_path in folder.glob("*.txt"):
        docs[file_path.name] = load_text_file(str(file_path))

    if not docs:
        raise ValueError(f"No .txt files found in: {folder_path}")

    return docs
