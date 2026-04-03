from __future__ import annotations

import argparse
from pathlib import Path

from ml_models.yield_prediction.pipeline import YieldPipelineConfig, train_and_persist


FEATURES = [
    "rainfall_mm",
    "temperature_c",
    "soil_ph",
    "nitrogen",
    "phosphorus",
    "potassium",
    "nutrient_score",
    "water_stress_index",
]
TARGET = "yield_tph"


def train(
    dataset_path: Path = Path("datasets/processed/training_agri.csv"),
    artifact_path: Path = Path("ml_models/artifacts/yield_model.joblib"),
    bundle_artifact_path: Path = Path("ml_models/artifacts/yield_model_bundle.joblib"),
    cv_folds: int = 5,
) -> dict:
    config = YieldPipelineConfig(
        feature_columns=FEATURES,
        target_column=TARGET,
        cv_folds=cv_folds,
    )
    result = train_and_persist(
        dataset_path=dataset_path,
        best_artifact_path=artifact_path,
        bundle_artifact_path=bundle_artifact_path,
        config=config,
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train crop-yield models and persist artifacts.")
    parser.add_argument("--dataset-path", type=Path, default=Path("datasets/processed/training_agri.csv"))
    parser.add_argument("--artifact-path", type=Path, default=Path("ml_models/artifacts/yield_model.joblib"))
    parser.add_argument("--bundle-artifact-path", type=Path, default=Path("ml_models/artifacts/yield_model_bundle.joblib"))
    parser.add_argument("--cv-folds", type=int, default=5)
    args = parser.parse_args()

    summary = train(
        dataset_path=args.dataset_path,
        artifact_path=args.artifact_path,
        bundle_artifact_path=args.bundle_artifact_path,
        cv_folds=args.cv_folds,
    )
    print(f"Yield model pipeline complete: {summary}")
