from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from rag_assistant.embeddings.build_embeddings import embed_documents
from rag_assistant.embeddings.dataset_embedder import load_agricultural_records

try:
    from langchain_community.vectorstores import FAISS as LangchainFAISS
    from langchain_huggingface import HuggingFaceEmbeddings
except Exception:  # pragma: no cover
    LangchainFAISS = None
    HuggingFaceEmbeddings = None


def _normalize_records(records: list[dict] | None = None, dataset_paths: list[str | Path] | None = None) -> list[dict]:
    if records is not None:
        return records
    return load_agricultural_records(dataset_paths=dataset_paths)


def _normalize_loaded_documents(raw_docs: list) -> list[dict]:
    docs: list[dict] = []
    for item in raw_docs:
        if isinstance(item, dict):
            text = str(item.get("text", "")).strip()
            if text:
                docs.append({"text": text, "metadata": item.get("metadata", {})})
            continue
        text = str(item).strip()
        if text:
            docs.append({"text": text, "metadata": {}})
    return docs


def build_vector_store(
    index_dir: str | Path = Path("rag_assistant/vector_db/faiss_index"),
    records: list[dict] | None = None,
    dataset_paths: list[str | Path] | None = None,
) -> dict[str, str | int]:
    index_path = Path(index_dir)
    index_path.mkdir(parents=True, exist_ok=True)

    docs = _normalize_records(records=records, dataset_paths=dataset_paths)
    texts = [item["text"] for item in docs]
    metadata = [item.get("metadata", {}) for item in docs]

    metadata_path = index_path / "metadata.json"
    metadata_path.write_text(json.dumps({"documents": docs}, indent=2), encoding="utf-8")

    if LangchainFAISS is not None and HuggingFaceEmbeddings is not None:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        store = LangchainFAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadata)
        store.save_local(str(index_path))
        return {"mode": "langchain-faiss", "index_dir": str(index_path), "documents": len(docs)}

    vectors = embed_documents(texts).astype("float32")
    np.save(index_path / "fallback_vectors.npy", vectors)
    return {"mode": "numpy-fallback", "index_dir": str(index_path), "documents": len(docs)}


def query_vector_store(
    query: str,
    top_k: int = 4,
    index_dir: str | Path = Path("rag_assistant/vector_db/faiss_index"),
) -> list[dict]:
    index_path = Path(index_dir)
    metadata_path = index_path / "metadata.json"
    if not metadata_path.exists():
        return []

    docs = _normalize_loaded_documents(json.loads(metadata_path.read_text(encoding="utf-8")).get("documents", []))
    if not docs:
        return []

    if LangchainFAISS is not None and HuggingFaceEmbeddings is not None:
        index_file = index_path / "index.faiss"
        if index_file.exists():
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            store = LangchainFAISS.load_local(
                folder_path=str(index_path),
                embeddings=embeddings,
                allow_dangerous_deserialization=True,
            )
            matches = store.similarity_search(query, k=top_k)
            return [
                {
                    "text": match.page_content,
                    "metadata": match.metadata or {},
                }
                for match in matches
            ]

    vectors_path = index_path / "fallback_vectors.npy"
    if not vectors_path.exists():
        return docs[:top_k]

    vectors = np.load(vectors_path)
    query_vector = embed_documents([query]).astype("float32")[0]
    scores = vectors @ query_vector
    indices = np.argsort(-scores)[:top_k]
    return [docs[int(i)] for i in indices]
