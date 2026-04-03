from __future__ import annotations

import pandas as pd


def build_risk_index(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    frame["risk_index"] = (
        frame.get("drought_index", 0.0) * 0.5
        + (1 - frame.get("avg_ndvi", 0.5)) * 0.3
        + frame.get("pest_incidence", 0.0) * 0.2
    )
    return frame
