from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

from climate_forecasting.arima_model.forecast import forecast_with_arima
from climate_forecasting.prophet_model.forecast import forecast_with_prophet
from ml_models.common.io import load_artifact, save_artifact

try:
    from prophet import Prophet
except Exception:  # pragma: no cover
    Prophet = None


DEFAULT_ARTIFACT_PATH = Path("ml_models/artifacts/productivity_forecaster.joblib")
DEFAULT_DATASET_PATH = Path("datasets/processed/productivity_history.csv")


def _load_history(dataset_path: Path, region_id: str) -> pd.DataFrame:
    frame = pd.read_csv(dataset_path)
    if "region_id" in frame.columns:
        filtered = frame[frame["region_id"] == region_id].copy()
        if not filtered.empty:
            frame = filtered

    required = {"date", "rainfall_mm", "temperature_c"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns for productivity forecasting: {sorted(missing)}")

    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["rainfall_mm"] = pd.to_numeric(frame["rainfall_mm"], errors="coerce")
    frame["temperature_c"] = pd.to_numeric(frame["temperature_c"], errors="coerce")

    if "productivity_index" not in frame.columns:
        if "yield_tph" in frame.columns:
            frame["productivity_index"] = pd.to_numeric(frame["yield_tph"], errors="coerce")
        else:
            # Fallback proxy from rainfall and temperature trends.
            frame["productivity_index"] = (
                frame["rainfall_mm"] * 0.018 + (35 - frame["temperature_c"]).clip(lower=0) * 0.07
            )

    frame["productivity_index"] = pd.to_numeric(frame["productivity_index"], errors="coerce")
    frame = frame.dropna(subset=["date", "rainfall_mm", "temperature_c", "productivity_index"]).sort_values("date")
    if len(frame) < 6:
        raise ValueError("At least 6 time points are required for productivity forecasting.")
    return frame.reset_index(drop=True)


def _blend_climate_inputs(region_id: str, horizon_days: int) -> pd.DataFrame:
    arima_points = forecast_with_arima(region_id, horizon_days)
    prophet_points = forecast_with_prophet(region_id, horizon_days)

    rows = []
    for arima_point, prophet_point in zip(arima_points, prophet_points, strict=False):
        rows.append(
            {
                "date": arima_point["date"],
                "rainfall_mm": (arima_point["rainfall_mm"] + prophet_point["rainfall_mm"]) / 2,
                "temperature_c": (arima_point["temperature_c"] + prophet_point["temperature_c"]) / 2,
            }
        )
    return pd.DataFrame(rows)


def train_productivity_models(
    dataset_path: Path = DEFAULT_DATASET_PATH,
    region_id: str = "delhi-ncr",
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
) -> dict:
    history = _load_history(dataset_path=dataset_path, region_id=region_id)

    arima_model = ARIMA(
        endog=history["productivity_index"],
        exog=history[["rainfall_mm", "temperature_c"]],
        order=(2, 1, 1),
    ).fit()

    prophet_model = None
    prophet_status = "not_available"
    if Prophet is not None:
        prophet_train = history[["date", "productivity_index", "rainfall_mm", "temperature_c"]].rename(
            columns={"date": "ds", "productivity_index": "y"}
        )
        prophet_model = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=True)
        prophet_model.add_regressor("rainfall_mm")
        prophet_model.add_regressor("temperature_c")
        prophet_model.fit(prophet_train)
        prophet_status = "trained"

    payload = {
        "region_id": region_id,
        "arima_model": arima_model,
        "prophet_model": prophet_model,
        "prophet_status": prophet_status,
        "history_end_date": str(history["date"].max().date()),
        "model_name": "productivity_arima_prophet",
    }
    save_artifact(payload, artifact_path)

    return {
        "status": "trained",
        "region_id": region_id,
        "samples": len(history),
        "prophet_status": prophet_status,
        "artifact_path": str(artifact_path),
    }


def forecast_crop_productivity(
    region_id: str,
    horizon_days: int,
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
) -> list[dict]:
    climate_inputs = _blend_climate_inputs(region_id=region_id, horizon_days=horizon_days)
    if climate_inputs.empty:
        return []

    artifact = load_artifact(artifact_path)
    if artifact is None:
        # Heuristic fallback when model is not trained yet.
        output = []
        for row in climate_inputs.to_dict(orient="records"):
            productivity = row["rainfall_mm"] * 0.018 + max(0.0, 35 - row["temperature_c"]) * 0.07
            output.append(
                {
                    "date": row["date"],
                    "rainfall_mm": round(float(row["rainfall_mm"]), 2),
                    "temperature_c": round(float(row["temperature_c"]), 2),
                    "productivity_arima": round(float(productivity), 3),
                    "productivity_prophet": round(float(productivity), 3),
                    "productivity_blended": round(float(productivity), 3),
                }
            )
        return output

    exog_future = climate_inputs[["rainfall_mm", "temperature_c"]]
    arima_values = artifact["arima_model"].forecast(steps=horizon_days, exog=exog_future)

    if artifact.get("prophet_model") is not None and artifact.get("prophet_status") == "trained":
        prophet_future = climate_inputs.rename(columns={"date": "ds"})[["ds", "rainfall_mm", "temperature_c"]]
        prophet_pred = artifact["prophet_model"].predict(prophet_future)
        prophet_values = prophet_pred["yhat"].to_numpy()
    else:
        prophet_values = arima_values.to_numpy()

    output = []
    for idx, row in climate_inputs.iterrows():
        arima_productivity = max(0.0, float(arima_values.iloc[idx]))
        prophet_productivity = max(0.0, float(prophet_values[idx]))
        blended = (arima_productivity + prophet_productivity) / 2
        point_date = row["date"]
        if isinstance(point_date, pd.Timestamp):
            point_date = point_date.date()
        if isinstance(point_date, str):
            point_date = pd.to_datetime(point_date).date()
        if not isinstance(point_date, date):
            point_date = date.today()

        output.append(
            {
                "date": point_date,
                "rainfall_mm": round(float(row["rainfall_mm"]), 2),
                "temperature_c": round(float(row["temperature_c"]), 2),
                "productivity_arima": round(arima_productivity, 3),
                "productivity_prophet": round(prophet_productivity, 3),
                "productivity_blended": round(blended, 3),
            }
        )

    return output
