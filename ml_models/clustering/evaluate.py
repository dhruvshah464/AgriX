from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics import silhouette_score

from ml_models.common.io import load_artifact


def run(dataset_path: Path = Path("datasets/processed/region_features.csv")) -> dict:
    artifact = load_artifact("ml_models/artifacts/region_cluster.joblib")
    if artifact is None:
        return {"status": "missing_model"}

    frame = pd.read_csv(dataset_path)
    X = frame[artifact["features"]]
    labels = artifact["model"].predict(X)
    score = silhouette_score(X, labels)
    return {"silhouette_score": float(score)}


if __name__ == "__main__":
    print(run())
