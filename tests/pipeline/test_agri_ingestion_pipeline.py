from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_pipeline.ingestion.agri_ingestion_pipeline import AgriDataIngestionPipeline, WeatherLocation


def test_agri_ingestion_pipeline_end_to_end(tmp_path: Path) -> None:
    faostat_csv = tmp_path / "faostat.csv"
    kaggle_csv = tmp_path / "kaggle.csv"
    db_path = tmp_path / "ingestion.db"

    pd.DataFrame(
        [
            {"Area": "India", "Item": "Wheat", "Year": 2024, "Value": 36000, "Unit": "hg/ha"},
            {"Area": "India", "Item": "Rice", "Year": 2024, "Value": 42000, "Unit": "hg/ha"},
        ]
    ).to_csv(faostat_csv, index=False)

    pd.DataFrame(
        [
            {"State_Name": "Punjab", "Crop_Year": 2024, "Crop": "Wheat", "Yield": 4.3},
            {"State_Name": "Bihar", "Crop_Year": 2024, "Crop": "Rice", "Yield": 4.7},
        ]
    ).to_csv(kaggle_csv, index=False)

    pipeline = AgriDataIngestionPipeline(database_url=f"sqlite:///{db_path}", weather_api_key=None)
    result = pipeline.run(
        locations=[WeatherLocation(region="Punjab", lat=30.9, lon=75.8), WeatherLocation(region="Bihar", lat=25.6, lon=85.1)],
        faostat_csv_path=faostat_csv,
        kaggle_dataset_path=kaggle_csv,
    )

    assert result["weather_rows"] == 2
    assert result["faostat_rows"] == 2
    assert result["kaggle_rows"] == 2
    assert result["normalized_rows"] == 4

    normalized = pd.read_sql_table("crop_yield_normalized", con=pipeline.engine)
    assert "yield_tph_norm" in normalized.columns
    assert normalized["yield_tph_norm"].between(0, 1).all()

    weather = pd.read_sql_table("weather_observations", con=pipeline.engine)
    assert set(["temperature_c_norm", "rainfall_mm_norm", "humidity_norm"]).issubset(weather.columns)
