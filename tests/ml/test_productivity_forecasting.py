from __future__ import annotations

from pathlib import Path

import pandas as pd

from climate_forecasting.productivity_forecasting.system import (
    forecast_crop_productivity,
    train_productivity_models,
)


def test_productivity_forecasting_with_arima_and_prophet(tmp_path: Path) -> None:
    dataset_path = tmp_path / "productivity_history.csv"
    artifact_path = tmp_path / "productivity_forecaster.joblib"

    frame = pd.DataFrame(
        [
            {"date": "2024-01-01", "region_id": "r1", "rainfall_mm": 42, "temperature_c": 18.5, "yield_tph": 2.6},
            {"date": "2024-02-01", "region_id": "r1", "rainfall_mm": 36, "temperature_c": 20.0, "yield_tph": 2.8},
            {"date": "2024-03-01", "region_id": "r1", "rainfall_mm": 29, "temperature_c": 24.3, "yield_tph": 3.0},
            {"date": "2024-04-01", "region_id": "r1", "rainfall_mm": 17, "temperature_c": 30.5, "yield_tph": 3.1},
            {"date": "2024-05-01", "region_id": "r1", "rainfall_mm": 20, "temperature_c": 34.0, "yield_tph": 3.0},
            {"date": "2024-06-01", "region_id": "r1", "rainfall_mm": 88, "temperature_c": 33.2, "yield_tph": 3.6},
            {"date": "2024-07-01", "region_id": "r1", "rainfall_mm": 170, "temperature_c": 31.0, "yield_tph": 4.2},
            {"date": "2024-08-01", "region_id": "r1", "rainfall_mm": 209, "temperature_c": 30.0, "yield_tph": 4.5},
            {"date": "2024-09-01", "region_id": "r1", "rainfall_mm": 143, "temperature_c": 29.1, "yield_tph": 4.3},
            {"date": "2024-10-01", "region_id": "r1", "rainfall_mm": 66, "temperature_c": 27.0, "yield_tph": 3.8},
            {"date": "2024-11-01", "region_id": "r1", "rainfall_mm": 21, "temperature_c": 22.0, "yield_tph": 3.3},
            {"date": "2024-12-01", "region_id": "r1", "rainfall_mm": 13, "temperature_c": 18.3, "yield_tph": 2.9},
        ]
    )
    frame.to_csv(dataset_path, index=False)

    train_result = train_productivity_models(
        dataset_path=dataset_path,
        region_id="r1",
        artifact_path=artifact_path,
    )
    assert train_result["status"] == "trained"
    assert artifact_path.exists()

    forecast_points = forecast_crop_productivity(region_id="r1", horizon_days=5, artifact_path=artifact_path)
    assert len(forecast_points) == 5
    for point in forecast_points:
        assert "productivity_arima" in point
        assert "productivity_prophet" in point
        assert "productivity_blended" in point
        assert point["productivity_blended"] >= 0
