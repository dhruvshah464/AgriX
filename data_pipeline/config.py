from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class PipelineConfig:
    raw_dir: Path = Path("datasets/raw")
    processed_dir: Path = Path("datasets/processed")
    external_dir: Path = Path("datasets/external")

    weather_dataset: Path = Path("datasets/raw/weather_history.csv")
    crop_dataset: Path = Path("datasets/raw/crop_yield.csv")
    soil_dataset: Path = Path("datasets/raw/soil_health.csv")

    training_dataset: Path = Path("datasets/processed/training_agri.csv")


config = PipelineConfig()
