from __future__ import annotations

import pandas as pd


NUMERIC_COLUMNS = [
    "rainfall_mm",
    "temperature_c",
    "soil_ph",
    "nitrogen",
    "phosphorus",
    "potassium",
    "yield_tph",
]


def clean_agri_frame(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.copy()
    for col in NUMERIC_COLUMNS:
        if col in clean_df.columns:
            clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce")
            clean_df[col] = clean_df[col].fillna(clean_df[col].median())

    if "crop" in clean_df.columns:
        clean_df["crop"] = clean_df["crop"].fillna("unknown").str.lower().str.strip()

    clean_df = clean_df.drop_duplicates().reset_index(drop=True)
    return clean_df


if __name__ == "__main__":
    frame = pd.read_csv("datasets/raw/crop_yield.csv")
    cleaned = clean_agri_frame(frame)
    cleaned.to_csv("datasets/processed/crop_yield_clean.csv", index=False)
    print("Data cleaned to datasets/processed/crop_yield_clean.csv")
