from __future__ import annotations

from pathlib import Path

import pandas as pd

from backend.app.core.config import settings
from data_pipeline.ingestion.openweather_client import OpenWeatherClient


def run(lat: float = 28.6139, lon: float = 77.2090, out_path: Path = Path("datasets/raw/weather_history.csv")) -> Path:
    client = OpenWeatherClient(settings.OPENWEATHER_API_KEY)
    payload = client.fetch_current_weather(lat=lat, lon=lon)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame([payload])
    if out_path.exists():
        existing = pd.read_csv(out_path)
        frame = pd.concat([existing, frame], ignore_index=True)
    frame.to_csv(out_path, index=False)
    return out_path


if __name__ == "__main__":
    file_path = run()
    print(f"Weather data ingested: {file_path}")
