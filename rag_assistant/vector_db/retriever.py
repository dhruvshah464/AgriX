from __future__ import annotations

from pathlib import Path

from rag_assistant.vector_db.langchain_faiss_store import query_vector_store


def retrieve_documents(
    query: str,
    top_k: int = 4,
    index_dir: Path = Path("rag_assistant/vector_db/faiss_index"),
) -> list[dict]:
    return query_vector_store(query=query, top_k=top_k, index_dir=index_dir)


def retrieve(query: str, top_k: int = 3, index_dir: Path = Path("rag_assistant/vector_db/faiss_index")) -> list[str]:
    return [item["text"] for item in retrieve_documents(query=query, top_k=top_k, index_dir=index_dir)]
