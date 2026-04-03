from __future__ import annotations

import pandas as pd


def classify_soil_zones(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    ph = frame.get("soil_ph", 7)
    frame["soil_zone"] = pd.cut(ph, bins=[0, 5.5, 7.5, 14], labels=["acidic", "neutral", "alkaline"])
    return frame
