from __future__ import annotations

import pandas as pd
from sklearn.preprocessing import MinMaxScaler


FEATURE_COLUMNS = ["rainfall_mm", "temperature_c", "soil_ph", "nitrogen", "phosphorus", "potassium"]


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    available = [col for col in FEATURE_COLUMNS if col in frame.columns]
    if not available:
        return frame

    scaler = MinMaxScaler()
    frame[available] = scaler.fit_transform(frame[available])
    return frame


if __name__ == "__main__":
    frame = pd.read_csv("datasets/processed/crop_yield_clean.csv")
    normalized = normalize(frame)
    normalized.to_csv("datasets/processed/crop_yield_normalized.csv", index=False)
    print("Data normalized to datasets/processed/crop_yield_normalized.csv")
