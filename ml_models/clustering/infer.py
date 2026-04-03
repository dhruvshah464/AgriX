from __future__ import annotations

from ml_models.common.io import load_artifact


def assign_cluster(payload: dict) -> int:
    artifact = load_artifact("ml_models/artifacts/region_cluster.joblib")
    if artifact is None:
        # Fallback segmentation by NDVI.
        ndvi = payload.get("avg_ndvi", 0.0)
        if ndvi >= 0.7:
            return 0
        if ndvi >= 0.5:
            return 1
        if ndvi >= 0.3:
            return 2
        return 3

    vector = [[payload.get(name, 0.0) for name in artifact["features"]]]
    return int(artifact["model"].predict(vector)[0])
