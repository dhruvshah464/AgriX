from __future__ import annotations

from ml_models.common.io import load_artifact


def infer_crop_suitability(payload: dict) -> tuple[str, float]:
    artifact = load_artifact("ml_models/artifacts/crop_classifier.joblib")
    if artifact is None:
        # Rule-based fallback
        if payload.get("rainfall_mm", 0) > 150 and payload.get("temperature_c", 0) > 24:
            return "rice", 0.55
        if payload.get("soil_ph", 7) < 6.5:
            return "potato", 0.52
        return "wheat", 0.54

    vector = [[payload.get(name, 0.0) for name in artifact["features"]]]
    probs = artifact["model"].predict_proba(vector)[0]
    idx = int(probs.argmax())
    return str(artifact["classes"][idx]), float(round(probs[idx], 3))
