from __future__ import annotations

from pathlib import Path

import pandas as pd

from ml_models.common.io import save_artifact

try:
    from prophet import Prophet
except Exception:  # pragma: no cover
    Prophet = None


def train(dataset_path: Path = Path("datasets/processed/climate_history.csv"), artifact_path: Path = Path("ml_models/artifacts/prophet_climate.joblib")) -> dict:
    frame = pd.read_csv(dataset_path)
    if Prophet is None:
        save_artifact({"status": "prophet_not_available"}, artifact_path)
        return {"status": "prophet_not_available"}

    rain = frame[["date", "rainfall_mm"]].rename(columns={"date": "ds", "rainfall_mm": "y"})
    temp = frame[["date", "temperature_c"]].rename(columns={"date": "ds", "temperature_c": "y"})

    rain_model = Prophet(daily_seasonality=True)
    temp_model = Prophet(daily_seasonality=True)
    rain_model.fit(rain)
    temp_model.fit(temp)

    save_artifact({"rain_model": rain_model, "temp_model": temp_model, "model_name": "prophet"}, artifact_path)
    return {"status": "trained", "samples": len(frame)}


if __name__ == "__main__":
    print(train())
