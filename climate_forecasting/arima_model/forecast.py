from __future__ import annotations

from datetime import date, timedelta

from ml_models.common.io import load_artifact


def forecast_with_arima(region_id: str, horizon_days: int) -> list[dict]:
    artifact = load_artifact("ml_models/artifacts/arima_climate.joblib")
    today = date.today()

    if artifact is None:
        points = []
        for i in range(horizon_days):
            points.append(
                {
                    "region_id": region_id,
                    "date": today + timedelta(days=i + 1),
                    "rainfall_mm": 60 + (i % 5) * 4,
                    "temperature_c": 28 + (i % 7) * 0.35,
                    "drought_index": round(0.35 + (i % 6) * 0.03, 3),
                }
            )
        return points

    rain_forecast = artifact["rain_model"].forecast(steps=horizon_days)
    temp_forecast = artifact["temp_model"].forecast(steps=horizon_days)

    points = []
    for idx in range(horizon_days):
        rainfall = float(max(0.0, rain_forecast.iloc[idx]))
        temp = float(temp_forecast.iloc[idx])
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
