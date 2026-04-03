from __future__ import annotations

import pandas as pd

from data_pipeline.feature_engineering.build_features import build
from data_pipeline.feature_engineering.spatial_features import add_spatial_features
from data_pipeline.feature_engineering.temporal_features import add_temporal_features
from data_pipeline.ingestion.ingest_market import run as ingest_market
from data_pipeline.ingestion.ingest_satellite import run as ingest_satellite
from data_pipeline.ingestion.ingest_weather import run as ingest_weather
from data_pipeline.preprocessing.clean_data import clean_agri_frame
from data_pipeline.preprocessing.normalize_data import normalize


def run_full_pipeline() -> str:
    ingest_weather()
    ingest_market()
    ingest_satellite()

    raw = pd.read_csv("datasets/raw/crop_yield.csv")
    cleaned = clean_agri_frame(raw)
    normalized = normalize(cleaned)
    featured = add_temporal_features(add_spatial_features(build(normalized)))
    featured.to_csv("datasets/processed/training_agri.csv", index=False)
    return "datasets/processed/training_agri.csv"


if __name__ == "__main__":
    output = run_full_pipeline()
    print(f"Pipeline output: {output}")
