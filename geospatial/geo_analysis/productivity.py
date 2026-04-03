from __future__ import annotations

from pathlib import Path

import pandas as pd


def build_productivity_geojson(
    region_id: str,
    dataset_path: Path = Path("datasets/processed/region_productivity.csv"),
    climate_path: Path = Path("datasets/processed/climate_history.csv"),
) -> dict:
    if dataset_path.exists():
        frame = pd.read_csv(dataset_path)
        if "region_id" in frame.columns:
            frame = frame[frame["region_id"] == region_id]
    else:
        frame = pd.DataFrame(
            [
                {"region_id": region_id, "latitude": 28.63, "longitude": 77.21, "yield_tph": 3.7, "avg_ndvi": 0.58},
                {"region_id": region_id, "latitude": 28.65, "longitude": 77.23, "yield_tph": 4.2, "avg_ndvi": 0.64},
            ]
        )

    if climate_path.exists():
        climate = pd.read_csv(climate_path)
        if {"region_id", "rainfall_mm"}.issubset(climate.columns):
            rainfall = climate.groupby("region_id", as_index=False)["rainfall_mm"].mean().rename(
                columns={"rainfall_mm": "avg_rainfall_mm"}
            )
            frame = frame.merge(rainfall, on="region_id", how="left")

    if "avg_rainfall_mm" not in frame.columns:
        frame["avg_rainfall_mm"] = 0.0

    features = []
    for row in frame.to_dict(orient="records"):
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "region_id": row.get("region_id"),
                    "yield_tph": row.get("yield_tph"),
                    "avg_ndvi": row.get("avg_ndvi"),
                    "avg_rainfall_mm": row.get("avg_rainfall_mm", 0.0),
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(row.get("longitude", 0.0)), float(row.get("latitude", 0.0))],
                },
            }
        )

    return {"type": "FeatureCollection", "features": features}
