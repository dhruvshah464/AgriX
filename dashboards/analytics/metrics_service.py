from __future__ import annotations

from pathlib import Path

import pandas as pd


def compute_kpis_from_frame(frame: pd.DataFrame) -> dict[str, float]:
    if frame.empty:
        return {"avg_yield": 0.0, "water_efficiency": 0.0, "disease_risk_index": 0.0}

    avg_yield = float(pd.to_numeric(frame.get("yield_tph", pd.Series([0.0])), errors="coerce").fillna(0.0).mean())
    rainfall = pd.to_numeric(frame.get("rainfall_mm", pd.Series([1.0])), errors="coerce").fillna(1.0)
    yield_series = pd.to_numeric(frame.get("yield_tph", pd.Series([0.0])), errors="coerce").fillna(0.0)
    water_efficiency = float((yield_series / rainfall.clip(lower=1)).mean() * 100)

    water_stress = pd.to_numeric(frame.get("water_stress_index", pd.Series([0.5])), errors="coerce").fillna(0.5)
    disease_risk = float((1 - water_stress.clip(0, 1)).mean())

    return {
        "avg_yield": round(avg_yield, 3),
        "water_efficiency": round(water_efficiency, 3),
        "disease_risk_index": round(disease_risk, 3),
    }


def compute_kpis(dataset_path: Path = Path("datasets/processed/training_agri.csv")) -> dict[str, float]:
    if not dataset_path.exists():
        return {"avg_yield": 0.0, "water_efficiency": 0.0, "disease_risk_index": 0.0}
    return compute_kpis_from_frame(pd.read_csv(dataset_path))
