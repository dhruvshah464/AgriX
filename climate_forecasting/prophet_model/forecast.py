from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from ml_models.common.io import load_artifact


def forecast_with_prophet(region_id: str, horizon_days: int) -> list[dict]:
    artifact = load_artifact("ml_models/artifacts/prophet_climate.joblib")
    today = date.today()

    if artifact is None or artifact.get("status") == "prophet_not_available":
        points = []
        for i in range(horizon_days):
            points.append(
                {
                    "region_id": region_id,
                    "date": today + timedelta(days=i + 1),
                    "rainfall_mm": 58 + (i % 4) * 5,
                    "temperature_c": 27.5 + (i % 5) * 0.4,
                    "drought_index": round(0.32 + (i % 6) * 0.025, 3),
                }
            )
        return points

    future = artifact["rain_model"].make_future_dataframe(periods=horizon_days)
    rain_forecast = artifact["rain_model"].predict(future).tail(horizon_days)
    temp_forecast = artifact["temp_model"].predict(future).tail(horizon_days)

    points = []
    for idx in range(horizon_days):
        rainfall = float(max(0.0, rain_forecast.iloc[idx]["yhat"]))
        temp = float(temp_forecast.iloc[idx]["yhat"])
        drought = max(0.0, min(1.0, (temp - rainfall / 10) / 50))
        points.append(
            {
                "region_id": region_id,
                "date": today + timedelta(days=idx + 1),
                "rainfall_mm": round(rainfall, 2),
                "temperature_c": round(temp, 2),
                "drought_index": round(drought, 3),
            }
        )
    return points
