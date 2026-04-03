from __future__ import annotations

from pathlib import Path

from rag_assistant.vector_db.langchain_faiss_store import build_vector_store


def build_index(
    index_dir: Path = Path("rag_assistant/vector_db/faiss_index"),
    dataset_paths: list[str | Path] | None = None,
) -> Path:
    build_vector_store(index_dir=index_dir, dataset_paths=dataset_paths)
    return index_dir
