from __future__ import annotations

import pandas as pd


SEASON_MAP = {"kharif": 1, "rabi": 2, "zaid": 3}


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    if "season" in frame.columns:
        frame["season_code"] = frame["season"].str.lower().map(SEASON_MAP).fillna(0)
    if "year" in frame.columns:
        frame["year_norm"] = (frame["year"] - frame["year"].min()) / (frame["year"].max() - frame["year"].min() + 1)
    return frame
