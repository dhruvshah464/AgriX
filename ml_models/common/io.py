from __future__ import annotations

from pathlib import Path

import joblib


def save_artifact(payload: dict, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, target)
    return target


def load_artifact(path: str | Path) -> dict | None:
    target = Path(path)
    if not target.exists():
        return None
    return joblib.load(target)
