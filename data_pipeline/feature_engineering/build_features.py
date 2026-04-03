from __future__ import annotations

import pandas as pd


def build(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()

    # Domain-driven synthetic feature for combined nutrient availability.
    frame["nutrient_score"] = (
        frame.get("nitrogen", 0) * 0.4
        + frame.get("phosphorus", 0) * 0.3
        + frame.get("potassium", 0) * 0.3
    )
    frame["water_stress_index"] = frame.get("temperature_c", 0) / (frame.get("rainfall_mm", 0) + 1)
    return frame


if __name__ == "__main__":
    data = pd.read_csv("datasets/processed/crop_yield_normalized.csv")
    features = build(data)
    features.to_csv("datasets/processed/training_agri.csv", index=False)
    print("Feature engineering complete: datasets/processed/training_agri.csv")
