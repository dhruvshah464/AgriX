from __future__ import annotations

import pandas as pd


def add_spatial_features(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    if {"latitude", "longitude"}.issubset(frame.columns):
        frame["lat_lon_interaction"] = frame["latitude"] * frame["longitude"]
    return frame
