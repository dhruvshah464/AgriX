from __future__ import annotations

from rag_assistant.embeddings.build_embeddings import load_knowledge_documents

try:
    from langchain_community.vectorstores import FAISS
    from langchain_core.documents import Document
    from langchain_huggingface import HuggingFaceEmbeddings
except Exception:  # pragma: no cover
    FAISS = None
    Document = None
    HuggingFaceEmbeddings = None


def build_langchain_store():
    if FAISS is None or Document is None or HuggingFaceEmbeddings is None:
        return None

    docs = [Document(page_content=text) for text in load_knowledge_documents()]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(docs, embeddings)
