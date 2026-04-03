from __future__ import annotations

from pathlib import Path

import pandas as pd

from ml_models.common.io import load_artifact
from ml_models.yield_prediction.train import train


def test_yield_pipeline_trains_evaluates_and_persists(tmp_path: Path) -> None:
    dataset_path = tmp_path / "training_agri.csv"
    best_artifact_path = tmp_path / "yield_model.joblib"
    bundle_artifact_path = tmp_path / "yield_model_bundle.joblib"

    frame = pd.DataFrame(
        [
            {"rainfall_mm": 50, "temperature_c": 20, "soil_ph": 6.3, "nitrogen": 55, "phosphorus": 30, "potassium": 36, "nutrient_score": 42.1, "water_stress_index": 0.39, "yield_tph": 2.1},
            {"rainfall_mm": 65, "temperature_c": 22, "soil_ph": 6.4, "nitrogen": 59, "phosphorus": 33, "potassium": 39, "nutrient_score": 45.2, "water_stress_index": 0.34, "yield_tph": 2.5},
            {"rainfall_mm": 80, "temperature_c": 24, "soil_ph": 6.5, "nitrogen": 63, "phosphorus": 36, "potassium": 42, "nutrient_score": 48.3, "water_stress_index": 0.30, "yield_tph": 2.9},
            {"rainfall_mm": 95, "temperature_c": 25, "soil_ph": 6.6, "nitrogen": 67, "phosphorus": 39, "potassium": 45, "nutrient_score": 51.4, "water_stress_index": 0.27, "yield_tph": 3.2},
            {"rainfall_mm": 110, "temperature_c": 27, "soil_ph": 6.7, "nitrogen": 71, "phosphorus": 42, "potassium": 48, "nutrient_score": 54.5, "water_stress_index": 0.24, "yield_tph": 3.6},
            {"rainfall_mm": 125, "temperature_c": 28, "soil_ph": 6.8, "nitrogen": 75, "phosphorus": 45, "potassium": 51, "nutrient_score": 57.6, "water_stress_index": 0.22, "yield_tph": 4.0},
            {"rainfall_mm": 140, "temperature_c": 29, "soil_ph": 6.9, "nitrogen": 79, "phosphorus": 48, "potassium": 54, "nutrient_score": 60.7, "water_stress_index": 0.21, "yield_tph": 4.3},
            {"rainfall_mm": 155, "temperature_c": 30, "soil_ph": 7.0, "nitrogen": 83, "phosphorus": 51, "potassium": 57, "nutrient_score": 63.8, "water_stress_index": 0.19, "yield_tph": 4.6},
            {"rainfall_mm": 170, "temperature_c": 31, "soil_ph": 7.1, "nitrogen": 87, "phosphorus": 54, "potassium": 60, "nutrient_score": 66.9, "water_stress_index": 0.18, "yield_tph": 4.9},
            {"rainfall_mm": 185, "temperature_c": 32, "soil_ph": 7.2, "nitrogen": 91, "phosphorus": 57, "potassium": 63, "nutrient_score": 70.0, "water_stress_index": 0.17, "yield_tph": 5.1},
            {"rainfall_mm": 200, "temperature_c": 33, "soil_ph": 7.3, "nitrogen": 95, "phosphorus": 60, "potassium": 66, "nutrient_score": 73.1, "water_stress_index": 0.16, "yield_tph": 5.4},
            {"rainfall_mm": 215, "temperature_c": 34, "soil_ph": 7.4, "nitrogen": 99, "phosphorus": 63, "potassium": 69, "nutrient_score": 76.2, "water_stress_index": 0.15, "yield_tph": 5.7},
        ]
    )
    frame.to_csv(dataset_path, index=False)

    summary = train(
        dataset_path=dataset_path,
        artifact_path=best_artifact_path,
        bundle_artifact_path=bundle_artifact_path,
        cv_folds=4,
    )

    assert best_artifact_path.exists()
    assert bundle_artifact_path.exists()

    assert summary["model_name"] in {"linear_regression", "random_forest", "gradient_boosting"}
    assert set(summary["leaderboard"].keys()) == {"linear_regression", "random_forest", "gradient_boosting"}

    for model_name in summary["leaderboard"]:
        metrics = summary["leaderboard"][model_name]
        assert "rmse" in metrics
        assert "mae" in metrics
        assert "r2" in metrics
        assert "cv_rmse_mean" in metrics
        assert "cv_r2_mean" in metrics

    best_payload = load_artifact(best_artifact_path)
    assert best_payload is not None
    assert best_payload["model_name"] == summary["model_name"]
    assert "leaderboard" in best_payload

    bundle_payload = load_artifact(bundle_artifact_path)
    assert bundle_payload is not None
    assert set(bundle_payload["models"].keys()) == {"linear_regression", "random_forest", "gradient_boosting"}
