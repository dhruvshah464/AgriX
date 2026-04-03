from __future__ import annotations

from pathlib import Path

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

from ml_models.common.io import save_artifact


def train(dataset_path: Path = Path("datasets/processed/climate_history.csv"), artifact_path: Path = Path("ml_models/artifacts/arima_climate.joblib")) -> dict:
    frame = pd.read_csv(dataset_path)
    rainfall_series = frame["rainfall_mm"]
    temp_series = frame["temperature_c"]

    rain_model = ARIMA(rainfall_series, order=(2, 1, 1)).fit()
    temp_model = ARIMA(temp_series, order=(2, 1, 1)).fit()

    payload = {
        "rain_model": rain_model,
        "temp_model": temp_model,
        "model_name": "arima(2,1,1)",
    }
    save_artifact(payload, artifact_path)
    return {"status": "trained", "samples": len(frame)}


if __name__ == "__main__":
    print(train())
