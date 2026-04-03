from __future__ import annotations

from ml_models.common.io import load_artifact


def _heuristic_yield(payload: dict) -> float:
    nutrient = payload.get("nitrogen", 0) * 0.4 + payload.get("phosphorus", 0) * 0.3 + payload.get("potassium", 0) * 0.3
    rain_factor = payload.get("rainfall_mm", 0) / 100
    temp_penalty = max(0.0, (payload.get("temperature_c", 25) - 30) * 0.2)
    soil_factor = max(0.0, 1 - abs(payload.get("soil_ph", 7) - 6.5) / 7)
    return max(0.5, nutrient * 0.03 + rain_factor + soil_factor - temp_penalty)


def predict_yield(payload: dict) -> tuple[float, float, str]:
    artifact = load_artifact("ml_models/artifacts/yield_model.joblib")
    if artifact is None:
        return round(_heuristic_yield(payload), 3), 0.58, "heuristic"

    features = artifact["features"]
    vector = [[payload.get(name, 0.0) for name in features]]
    pred = float(artifact["model"].predict(vector)[0])
    confidence = max(0.5, min(0.98, artifact["metrics"].get("r2", 0.6)))
    return round(pred, 3), round(confidence, 3), artifact["model_name"]
