from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans

from ml_models.common.io import save_artifact


FEATURES = ["avg_rainfall_mm", "avg_temperature_c", "avg_ndvi", "soil_fertility_index"]


def train(dataset_path: Path = Path("datasets/processed/region_features.csv"), artifact_path: Path = Path("ml_models/artifacts/region_cluster.joblib"), n_clusters: int = 4) -> dict:
    frame = pd.read_csv(dataset_path)
    X = frame[[f for f in FEATURES if f in frame.columns]]

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    model.fit(X)

    payload = {"model": model, "features": list(X.columns), "model_name": "kmeans", "n_clusters": n_clusters}
    save_artifact(payload, artifact_path)
    return {"n_clusters": n_clusters, "samples": len(frame)}


if __name__ == "__main__":
    print(train())
