from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import zipfile
from urllib.request import urlopen

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from data_pipeline.ingestion.openweather_client import OpenWeatherClient


def _normalize_column_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def _column_lookup(columns: Iterable[str]) -> dict[str, str]:
    return {_normalize_column_name(col): col for col in columns}


def _pick_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    lookup = _column_lookup(df.columns)
    for candidate in candidates:
        key = _normalize_column_name(candidate)
        if key in lookup:
            return lookup[key]
    return None


def _min_max_normalize(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    min_val = numeric.min()
    max_val = numeric.max()
    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return pd.Series([0.0] * len(numeric), index=numeric.index, dtype="float64")
    return (numeric - min_val) / (max_val - min_val)


@dataclass(slots=True)
class WeatherLocation:
    region: str
    lat: float
    lon: float
    country: str = "India"


class AgriDataIngestionPipeline:
    def __init__(self, database_url: str | None = None, weather_api_key: str | None = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://agrix:agrix@localhost:5432/agrix",
        )
        self.engine: Engine = create_engine(self.database_url, pool_pre_ping=True)
        self.weather_client = OpenWeatherClient(weather_api_key or os.getenv("OPENWEATHER_API_KEY"))

    def fetch_weather_data(self, locations: Iterable[WeatherLocation]) -> pd.DataFrame:
        records: list[dict] = []
        for location in locations:
            payload = self.weather_client.fetch_current_weather(lat=location.lat, lon=location.lon)
            records.append(
                {
                    "region": location.region,
                    "country": location.country,
                    "latitude": location.lat,
                    "longitude": location.lon,
                    "observation_time": payload.get("timestamp"),
                    "temperature_c": payload.get("temperature_c"),
                    "rainfall_mm": payload.get("rainfall_mm"),
                    "humidity": payload.get("humidity"),
                    "source": "openweather",
                }
            )

        weather_df = pd.DataFrame(records)
        if weather_df.empty:
            return weather_df

        weather_df["observation_time"] = pd.to_datetime(weather_df["observation_time"], errors="coerce", utc=True)
        weather_df["temperature_c"] = pd.to_numeric(weather_df["temperature_c"], errors="coerce")
        weather_df["rainfall_mm"] = pd.to_numeric(weather_df["rainfall_mm"], errors="coerce")
        weather_df["humidity"] = pd.to_numeric(weather_df["humidity"], errors="coerce")

        for col in ["temperature_c", "rainfall_mm", "humidity"]:
            weather_df[f"{col}_norm"] = _min_max_normalize(weather_df[col])
        return weather_df

    def load_faostat_dataset(self, csv_path: str | Path | None = None, api_url: str | None = None) -> pd.DataFrame:
        if csv_path and Path(csv_path).exists():
            raw = pd.read_csv(csv_path)
        elif api_url:
            raw = self._load_remote_tabular(api_url)
        else:
            raw = pd.DataFrame(
                [
                    {"Area": "India", "Item": "Wheat", "Year": 2024, "Value": 34000, "Unit": "hg/ha"},
                    {"Area": "India", "Item": "Rice", "Year": 2024, "Value": 41000, "Unit": "hg/ha"},
                ]
            )
        standardized = self._standardize_crop_frame(raw, source="faostat", default_country="India")
        return standardized

    def load_kaggle_dataset(self, dataset_path: str | Path | None = None) -> pd.DataFrame:
        if dataset_path is None:
            raw = pd.DataFrame(
                [
                    {"State_Name": "Punjab", "Crop_Year": 2024, "Crop": "Wheat", "Yield": 4.2},
                    {"State_Name": "Uttar Pradesh", "Crop_Year": 2024, "Crop": "Rice", "Yield": 4.8},
                ]
            )
            return self._standardize_crop_frame(raw, source="kaggle", default_country="India")

        target = Path(dataset_path)
        if target.is_file():
            if target.suffix.lower() == ".zip":
                frames: list[pd.DataFrame] = []
                with zipfile.ZipFile(target, "r") as archive:
                    csv_members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
                    if not csv_members:
                        raise FileNotFoundError(f"No CSV files found in Kaggle ZIP archive: {target}")
                    for member in csv_members:
                        with archive.open(member) as handle:
                            frame = pd.read_csv(handle)
                            frames.append(self._standardize_crop_frame(frame, source="kaggle", default_country="India"))
                return pd.concat(frames, ignore_index=True)

            raw = pd.read_csv(target)
            return self._standardize_crop_frame(raw, source="kaggle", default_country="India")

        if target.is_dir():
            csv_files = sorted(target.rglob("*.csv"))
            if not csv_files:
                raise FileNotFoundError(f"No CSV files found under Kaggle dataset directory: {target}")
            frames = [self._standardize_crop_frame(pd.read_csv(file), source="kaggle", default_country="India") for file in csv_files]
            return pd.concat(frames, ignore_index=True)

        raise FileNotFoundError(f"Kaggle dataset path does not exist: {target}")

    def normalize_crop_data(self, crop_df: pd.DataFrame) -> pd.DataFrame:
        normalized = crop_df.copy()
        for col in ["yield_tph", "year", "rainfall_mm", "temperature_c", "humidity"]:
            if col in normalized.columns:
                normalized[col] = pd.to_numeric(normalized[col], errors="coerce")
                normalized[f"{col}_norm"] = _min_max_normalize(normalized[col])

        normalized["crop"] = normalized["crop"].astype(str).str.lower().str.strip()
        normalized["region"] = normalized["region"].fillna("unknown").astype(str).str.strip()
        normalized["country"] = normalized["country"].fillna("unknown").astype(str).str.strip()
        normalized["ingested_at"] = pd.Timestamp.utcnow()
        return normalized

    def attach_weather_to_crop(self, crop_df: pd.DataFrame, weather_df: pd.DataFrame) -> pd.DataFrame:
        if weather_df.empty:
            merged = crop_df.copy()
            for col in ["temperature_c", "rainfall_mm", "humidity"]:
                if col not in merged:
                    merged[col] = None
            return merged

        latest_weather = (
            weather_df.sort_values("observation_time")
            .drop_duplicates(subset=["region"], keep="last")
            .loc[:, ["region", "temperature_c", "rainfall_mm", "humidity"]]
        )
        merged = crop_df.merge(latest_weather, on="region", how="left")

        global_defaults = weather_df[["temperature_c", "rainfall_mm", "humidity"]].mean(numeric_only=True)
        for col in ["temperature_c", "rainfall_mm", "humidity"]:
            if col in merged.columns:
                merged[col] = merged[col].fillna(global_defaults.get(col))
        return merged

    def store_results(self, weather_df: pd.DataFrame, crop_raw_df: pd.DataFrame, crop_normalized_df: pd.DataFrame) -> None:
        run_at = pd.Timestamp.utcnow()

        weather_to_store = weather_df.copy()
        crop_raw_to_store = crop_raw_df.copy()
        crop_norm_to_store = crop_normalized_df.copy()

        if not weather_to_store.empty:
            weather_to_store["ingested_at"] = run_at
            weather_to_store.to_sql("weather_observations", con=self.engine, if_exists="append", index=False, method="multi")

        if not crop_raw_to_store.empty:
            crop_raw_to_store["ingested_at"] = run_at
            crop_raw_to_store.to_sql("crop_yield_raw", con=self.engine, if_exists="append", index=False, method="multi")

        if not crop_norm_to_store.empty:
            crop_norm_to_store.to_sql("crop_yield_normalized", con=self.engine, if_exists="append", index=False, method="multi")

    def run(
        self,
        locations: Iterable[WeatherLocation],
        faostat_csv_path: str | Path | None = None,
        faostat_api_url: str | None = None,
        kaggle_dataset_path: str | Path | None = None,
    ) -> dict[str, int]:
        weather_df = self.fetch_weather_data(locations)
        faostat_df = self.load_faostat_dataset(csv_path=faostat_csv_path, api_url=faostat_api_url)
        kaggle_df = self.load_kaggle_dataset(dataset_path=kaggle_dataset_path)

        crop_raw = pd.concat([faostat_df, kaggle_df], ignore_index=True)
        crop_with_weather = self.attach_weather_to_crop(crop_raw, weather_df)
        crop_normalized = self.normalize_crop_data(crop_with_weather)

        self.store_results(weather_df=weather_df, crop_raw_df=crop_raw, crop_normalized_df=crop_normalized)
        return {
            "weather_rows": len(weather_df),
            "faostat_rows": len(faostat_df),
            "kaggle_rows": len(kaggle_df),
            "normalized_rows": len(crop_normalized),
        }

    def _standardize_crop_frame(self, raw: pd.DataFrame, source: str, default_country: str) -> pd.DataFrame:
        frame = raw.copy()

        country_col = _pick_column(frame, ["country", "area", "nation"])
        region_col = _pick_column(frame, ["region", "state_name", "state", "district", "zone", "location", "area"])
        crop_col = _pick_column(frame, ["crop", "item", "commodity", "crop_name"])
        year_col = _pick_column(frame, ["year", "crop_year"])
        value_col = _pick_column(frame, ["yield_tph", "yield", "value", "crop_yield", "production_per_hectare"])
        unit_col = _pick_column(frame, ["unit", "units"])

        if value_col is None:
            raise ValueError(f"Could not find a yield/value column for source={source}.")

        standardized = pd.DataFrame(
            {
                "country": frame[country_col].fillna(default_country) if country_col else default_country,
                "region": frame[region_col].fillna("unknown") if region_col else "unknown",
                "crop": frame[crop_col].fillna("unknown") if crop_col else "unknown",
                "year": pd.to_numeric(frame[year_col], errors="coerce") if year_col else pd.Timestamp.utcnow().year,
                "yield_tph": self._convert_to_tonnes_per_hectare(
                    values=pd.to_numeric(frame[value_col], errors="coerce"),
                    units=frame[unit_col] if unit_col else None,
                ),
                "source": source,
            }
        )

        standardized["crop"] = standardized["crop"].astype(str).str.strip()
        standardized["region"] = standardized["region"].astype(str).str.strip()
        standardized["country"] = standardized["country"].astype(str).str.strip()
        standardized["year"] = standardized["year"].fillna(pd.Timestamp.utcnow().year).astype(int)
        standardized["yield_tph"] = pd.to_numeric(standardized["yield_tph"], errors="coerce")
        standardized = standardized.dropna(subset=["yield_tph"]).reset_index(drop=True)
        return standardized

    @staticmethod
    def _convert_to_tonnes_per_hectare(values: pd.Series, units: pd.Series | None) -> pd.Series:
        values = pd.to_numeric(values, errors="coerce").astype("float64")
        if units is None:
            return values

        unit_values = units.astype(str).str.lower()
        converted = values.copy()

        hg_mask = unit_values.str.contains("hg/ha", na=False)
        kg_mask = unit_values.str.contains("kg/ha", na=False)
        tonne_mask = unit_values.str.contains("t/ha|tonne/ha|tonnes/ha", na=False)

        converted.loc[hg_mask] = converted.loc[hg_mask] / 10000.0
        converted.loc[kg_mask] = converted.loc[kg_mask] / 1000.0
        converted.loc[tonne_mask] = converted.loc[tonne_mask]
        return converted

    @staticmethod
    def _load_remote_tabular(url: str) -> pd.DataFrame:
        try:
            return pd.read_csv(url)
        except Exception:
            with urlopen(url, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))

            if isinstance(payload, list):
                return pd.DataFrame(payload)

            if isinstance(payload, dict):
                for key in ["data", "items", "results"]:
                    if key in payload and isinstance(payload[key], list):
                        return pd.DataFrame(payload[key])

            raise ValueError("Remote FAOSTAT payload is not a supported CSV/JSON tabular format.")


def _default_locations() -> list[WeatherLocation]:
    return [
        WeatherLocation(region="delhi-ncr", lat=28.6139, lon=77.2090),
        WeatherLocation(region="punjab-central", lat=30.7333, lon=76.7794),
        WeatherLocation(region="up-east", lat=26.8467, lon=80.9462),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="AgriX ingestion pipeline for OpenWeather + FAOSTAT + Kaggle.")
    parser.add_argument("--database-url", type=str, default=None, help="SQLAlchemy database URL (PostgreSQL recommended).")
    parser.add_argument("--faostat-csv-path", type=str, default=None, help="Path to local FAOSTAT CSV.")
    parser.add_argument("--faostat-api-url", type=str, default=None, help="CSV-compatible FAOSTAT URL.")
    parser.add_argument("--kaggle-dataset-path", type=str, default=None, help="Path to Kaggle crop-yield CSV or directory.")
    args = parser.parse_args()

    pipeline = AgriDataIngestionPipeline(database_url=args.database_url)
    summary = pipeline.run(
        locations=_default_locations(),
        faostat_csv_path=args.faostat_csv_path,
        faostat_api_url=args.faostat_api_url,
        kaggle_dataset_path=args.kaggle_dataset_path,
    )
    print(f"Ingestion complete: {summary}")


if __name__ == "__main__":
    main()
