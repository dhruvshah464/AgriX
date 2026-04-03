from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

pytest.importorskip("geopandas")

from geospatial.map_generation.agrix_mapbox_visualization import AgriXMapboxVisualizer, VisualizationConfig


def test_geospatial_visualization_bundle_generation(tmp_path: Path) -> None:
    productivity_csv = tmp_path / "region_productivity.csv"
    climate_csv = tmp_path / "climate_history.csv"
    output_dir = tmp_path / "maps"

    pd.DataFrame(
        [
            {"region_id": "r1", "latitude": 28.63, "longitude": 77.21, "yield_tph": 3.9, "avg_ndvi": 0.56},
            {"region_id": "r2", "latitude": 30.90, "longitude": 75.85, "yield_tph": 4.4, "avg_ndvi": 0.68},
        ]
    ).to_csv(productivity_csv, index=False)

    pd.DataFrame(
        [
            {"date": "2025-01-01", "region_id": "r1", "rainfall_mm": 42, "temperature_c": 17.8},
            {"date": "2025-02-01", "region_id": "r1", "rainfall_mm": 38, "temperature_c": 20.2},
            {"date": "2025-01-01", "region_id": "r2", "rainfall_mm": 62, "temperature_c": 19.2},
            {"date": "2025-02-01", "region_id": "r2", "rainfall_mm": 58, "temperature_c": 22.2},
        ]
    ).to_csv(climate_csv, index=False)

    visualizer = AgriXMapboxVisualizer(
        VisualizationConfig(
            productivity_csv=productivity_csv,
            climate_csv=climate_csv,
            output_dir=output_dir,
        )
    )
    outputs = visualizer.build_visualization_bundle(mapbox_token="pk.test-token", output_dir=output_dir)

    assert outputs["crop_productivity"].exists()
    assert outputs["rainfall_heatmap"].exists()
    assert outputs["ndvi_vegetation"].exists()
    assert outputs["mapbox_style"].exists()
    assert outputs["mapbox_html"].exists()

    style = json.loads(outputs["mapbox_style"].read_text(encoding="utf-8"))
    layer_ids = {layer["id"] for layer in style["layers"]}
    assert "crop-productivity-fill" in layer_ids
    assert "rainfall-heatmap" in layer_ids
    assert "ndvi-vegetation-points" in layer_ids
