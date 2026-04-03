from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    from langchain_core.documents import Document
except Exception:  # pragma: no cover
    Document = None


DEFAULT_DATASET_PATHS = [
    Path("datasets/external/agri_knowledge.txt"),
    Path("datasets/raw/crop_yield.csv"),
    Path("datasets/processed/training_agri.csv"),
    Path("datasets/processed/climate_history.csv"),
    Path("datasets/processed/productivity_history.csv"),
]


def _frame_to_rows_text(frame: pd.DataFrame, source: Path, max_rows: int = 200) -> list[dict]:
    rows = []
    limited = frame.head(max_rows)
    for idx, row in limited.iterrows():
        payload = ", ".join(f"{col}={row[col]}" for col in limited.columns[:20])
        rows.append(
            {
                "text": f"Agricultural record from {source.name}: {payload}",
                "metadata": {"source": str(source), "row": int(idx)},
            }
        )
    return rows


def load_agricultural_records(dataset_paths: list[str | Path] | None = None) -> list[dict]:
    paths = [Path(p) for p in dataset_paths] if dataset_paths else DEFAULT_DATASET_PATHS
    docs: list[dict] = []

    for path in paths:
        if not path.exists():
            continue

        suffix = path.suffix.lower()
        if suffix in {".txt", ".md"}:
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                text = line.strip()
                if text:
                    docs.append({"text": text, "metadata": {"source": str(path), "line": line_no}})
            continue

        if suffix == ".csv":
            frame = pd.read_csv(path)
            docs.extend(_frame_to_rows_text(frame, source=path))
            continue

        if suffix == ".parquet":
            frame = pd.read_parquet(path)
            docs.extend(_frame_to_rows_text(frame, source=path))
            continue

    if not docs:
        docs = [
            {
                "text": "Use balanced NPK fertilization and soil testing to maintain crop productivity.",
                "metadata": {"source": "fallback"},
            },
            {
                "text": "Monitor rainfall and adjust irrigation to prevent water stress.",
                "metadata": {"source": "fallback"},
            },
        ]
    return docs


def load_agricultural_documents(dataset_paths: list[str | Path] | None = None):
    records = load_agricultural_records(dataset_paths=dataset_paths)
    if Document is None:
        return records
    return [Document(page_content=item["text"], metadata=item["metadata"]) for item in records]
