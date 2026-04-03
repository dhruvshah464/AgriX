from __future__ import annotations

from pathlib import Path

import pandas as pd

from rag_assistant.chatbot.assistant import ask_assistant
from rag_assistant.vector_db.index_manager import build_index
from rag_assistant.vector_db.langchain_faiss_store import build_vector_store, query_vector_store


def test_build_and_query_vector_store_fallback(tmp_path: Path, monkeypatch) -> None:
    import rag_assistant.vector_db.langchain_faiss_store as store_module

    monkeypatch.setattr(store_module, "LangchainFAISS", None)
    monkeypatch.setattr(store_module, "HuggingFaceEmbeddings", None)

    index_dir = tmp_path / "faiss_index"
    records = [
        {"text": "Wheat benefits from moderate irrigation and cool temperatures.", "metadata": {"source": "test"}},
        {"text": "Rice performs best with high rainfall and warm temperatures.", "metadata": {"source": "test"}},
        {"text": "Low NDVI can indicate crop stress.", "metadata": {"source": "test"}},
    ]

    summary = build_vector_store(index_dir=index_dir, records=records)
    assert summary["documents"] == 3
    assert (index_dir / "metadata.json").exists()
    assert (index_dir / "fallback_vectors.npy").exists()

    matches = query_vector_store("high rainfall crop", top_k=2, index_dir=index_dir)
    assert len(matches) == 2
    assert all("text" in item for item in matches)

    answer, sources = ask_assistant(
        query="Which crop suits high rainfall?",
        provider="none",
        model_name="none",
        api_key=None,
        index_dir=index_dir,
    )
    assert isinstance(answer, str) and len(answer) > 0
    assert len(sources) > 0


def test_build_index_from_agricultural_datasets(tmp_path: Path, monkeypatch) -> None:
    import rag_assistant.vector_db.langchain_faiss_store as store_module

    monkeypatch.setattr(store_module, "LangchainFAISS", None)
    monkeypatch.setattr(store_module, "HuggingFaceEmbeddings", None)

    csv_path = tmp_path / "crop_yield.csv"
    txt_path = tmp_path / "agri_notes.txt"
    index_dir = tmp_path / "index"

    pd.DataFrame(
        [
            {"region_id": "r1", "crop": "wheat", "rainfall_mm": 70, "temperature_c": 22, "yield_tph": 3.5},
            {"region_id": "r2", "crop": "rice", "rainfall_mm": 180, "temperature_c": 29, "yield_tph": 4.6},
        ]
    ).to_csv(csv_path, index=False)
    txt_path.write_text("Soil testing helps optimize fertilizer use.\n")

    output = build_index(index_dir=index_dir, dataset_paths=[csv_path, txt_path])
    assert output == index_dir
    assert (index_dir / "metadata.json").exists()
