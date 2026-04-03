from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


def _min_max(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    min_val = values.min()
    max_val = values.max()
    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return pd.Series([0.0] * len(values), index=values.index, dtype="float64")
    return (values - min_val) / (max_val - min_val)


@dataclass(slots=True)
class PreprocessorConfig:
    rainfall_col: str = "rainfall_mm"
    temperature_col: str = "temperature_c"
    soil_col: str = "soil_type"
    season_col: str = "season"
    region_col: str = "region_id"


class AgriculturalPreprocessor:
    def __init__(self, config: PreprocessorConfig | None = None):
        self.config = config or PreprocessorConfig()

    def handle_missing_values(self, frame: pd.DataFrame) -> pd.DataFrame:
        cleaned = frame.copy()

        # Normalize key weather columns to numeric first.
        for col in [self.config.rainfall_col, self.config.temperature_col]:
            if col in cleaned.columns:
                cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

        numeric_cols = cleaned.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            median = cleaned[col].median()
            cleaned[col] = cleaned[col].fillna(0.0 if pd.isna(median) else median)

        categorical_cols = cleaned.select_dtypes(exclude=["number"]).columns
        for col in categorical_cols:
            cleaned[col] = cleaned[col].fillna("unknown").astype(str).str.strip()

        return cleaned

    def normalize_weather(self, frame: pd.DataFrame) -> pd.DataFrame:
        normalized = frame.copy()
        if self.config.rainfall_col in normalized.columns:
            normalized[f"{self.config.rainfall_col}_norm"] = _min_max(normalized[self.config.rainfall_col])
        if self.config.temperature_col in normalized.columns:
            normalized[f"{self.config.temperature_col}_norm"] = _min_max(normalized[self.config.temperature_col])
        return normalized

    def encode_soil_types(self, frame: pd.DataFrame) -> pd.DataFrame:
        encoded = frame.copy()
        if self.config.soil_col not in encoded.columns:
            return encoded

        encoded[self.config.soil_col] = encoded[self.config.soil_col].fillna("unknown").str.lower().str.strip()
        dummies = pd.get_dummies(encoded[self.config.soil_col], prefix=self.config.soil_col)
        encoded = pd.concat([encoded, dummies], axis=1)
        encoded[f"{self.config.soil_col}_code"] = encoded[self.config.soil_col].astype("category").cat.codes
        return encoded

    def generate_seasonal_features(self, frame: pd.DataFrame) -> pd.DataFrame:
        featured = frame.copy()
        if self.config.season_col not in featured.columns or self.config.rainfall_col not in featured.columns:
            return featured

        featured[self.config.season_col] = featured[self.config.season_col].fillna("unknown").str.lower().str.strip()

        group_cols = [self.config.season_col]
        if self.config.region_col in featured.columns:
            group_cols = [self.config.region_col, self.config.season_col]

        featured["seasonal_rainfall_avg"] = (
            featured.groupby(group_cols, dropna=False)[self.config.rainfall_col].transform("mean").round(3)
        )
        return featured

    def preprocess(self, frame: pd.DataFrame) -> pd.DataFrame:
        processed = self.handle_missing_values(frame)
        processed = self.normalize_weather(processed)
        processed = self.encode_soil_types(processed)
        processed = self.generate_seasonal_features(processed)
        return processed


def preprocess_csv(
    input_path: str | Path,
    output_path: str | Path,
    config: PreprocessorConfig | None = None,
) -> Path:
    source = Path(input_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    frame = pd.read_csv(source)
    processed = AgriculturalPreprocessor(config=config).preprocess(frame)
    processed.to_csv(target, index=False)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess agricultural datasets.")
    parser.add_argument("--input", type=str, required=True, help="Input CSV path.")
    parser.add_argument("--output", type=str, required=True, help="Output CSV path.")
    args = parser.parse_args()

    result = preprocess_csv(args.input, args.output)
    print(f"Preprocessed dataset written to: {result}")


if __name__ == "__main__":
    main()
