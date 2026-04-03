from __future__ import annotations

from pathlib import Path

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover
    SentenceTransformer = None


def _hash_embed(text: str, dim: int = 384) -> np.ndarray:
    vec = np.zeros(dim, dtype="float32")
    for token in text.lower().split():
        vec[hash(token) % dim] += 1.0
    norm = np.linalg.norm(vec) + 1e-6
    return vec / norm


def embed_documents(documents: list[str]) -> np.ndarray:
    if SentenceTransformer is None:
        return np.vstack([_hash_embed(doc) for doc in documents])

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vectors = model.encode(documents, normalize_embeddings=True)
    return np.asarray(vectors, dtype="float32")


def load_knowledge_documents(path: Path = Path("datasets/external/agri_knowledge.txt")) -> list[str]:
    if not path.exists():
        return [
            "Rice requires high rainfall and warm temperatures.",
            "Wheat performs well in cooler climates with moderate irrigation.",
            "Low NDVI can indicate crop stress due to water or nutrient deficiency.",
        ]

    return [line.strip() for line in path.read_text().splitlines() if line.strip()]
