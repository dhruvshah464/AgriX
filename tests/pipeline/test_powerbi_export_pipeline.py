from __future__ import annotations

from pathlib import Path

import pandas as pd

from dashboards.powerbi_exports.export_pipeline import export_powerbi_ready_data


def test_powerbi_export_pipeline_generates_datasets_and_dashboards(tmp_path: Path) -> None:
    crop_path = tmp_path / "crop_yield.csv"
    climate_path = tmp_path / "climate_history.csv"
    productivity_history_path = tmp_path / "productivity_history.csv"
    output_dir = tmp_path / "powerbi"
    dashboard_dir = tmp_path / "dashboards"

    pd.DataFrame(
        [
            {"region_id": "r1", "season": "kharif", "year": 2024, "crop": "rice", "rainfall_mm": 180, "temperature_c": 29, "yield_tph": 4.4},
            {"region_id": "r1", "season": "rabi", "year": 2024, "crop": "wheat", "rainfall_mm": 72, "temperature_c": 21, "yield_tph": 3.6},
            {"region_id": "r2", "season": "kharif", "year": 2024, "crop": "rice", "rainfall_mm": 200, "temperature_c": 30, "yield_tph": 4.8},
            {"region_id": "r2", "season": "rabi", "year": 2024, "crop": "wheat", "rainfall_mm": 68, "temperature_c": 20, "yield_tph": 3.9},
            {"region_id": "r1", "season": "kharif", "year": 2025, "crop": "rice", "rainfall_mm": 188, "temperature_c": 30, "yield_tph": 4.5},
            {"region_id": "r1", "season": "rabi", "year": 2025, "crop": "wheat", "rainfall_mm": 70, "temperature_c": 20, "yield_tph": 3.7},
        ]
    ).to_csv(crop_path, index=False)

    pd.DataFrame(
        [
            {"date": "2024-01-01", "region_id": "r1", "rainfall_mm": 70, "temperature_c": 21},
            {"date": "2024-07-01", "region_id": "r1", "rainfall_mm": 180, "temperature_c": 29},
            {"date": "2024-01-01", "region_id": "r2", "rainfall_mm": 68, "temperature_c": 20},
            {"date": "2024-07-01", "region_id": "r2", "rainfall_mm": 200, "temperature_c": 30},
            {"date": "2025-01-01", "region_id": "r1", "rainfall_mm": 69, "temperature_c": 20},
            {"date": "2025-07-01", "region_id": "r1", "rainfall_mm": 189, "temperature_c": 30},
        ]
    ).to_csv(climate_path, index=False)

    pd.DataFrame(
        [
            {"date": "2024-01-01", "region_id": "r1", "rainfall_mm": 70, "temperature_c": 21, "yield_tph": 3.6},
            {"date": "2024-07-01", "region_id": "r1", "rainfall_mm": 180, "temperature_c": 29, "yield_tph": 4.4},
            {"date": "2025-01-01", "region_id": "r1", "rainfall_mm": 69, "temperature_c": 20, "yield_tph": 3.7},
            {"date": "2025-07-01", "region_id": "r1", "rainfall_mm": 189, "temperature_c": 30, "yield_tph": 4.5},
        ]
    ).to_csv(productivity_history_path, index=False)

    outputs = export_powerbi_ready_data(
        source_path=crop_path,
        output_dir=output_dir,
        climate_path=climate_path,
        productivity_history_path=productivity_history_path,
        dashboard_output_dir=dashboard_dir,
    )

    required_paths = [
        "crop_productivity_trends",
        "rainfall_correlation_observations",
        "rainfall_correlation_summary",
        "climate_impact_analysis",
        "kpis",
        "powerbi_dataset",
        "powerbi_manifest",
        "dashboard_productivity",
        "dashboard_rainfall",
        "dashboard_climate_impact",
    ]
    for key in required_paths:
        assert outputs[key].exists(), f"Expected output file for key '{key}'"

    trends = pd.read_csv(outputs["crop_productivity_trends"])
    assert {"date", "region_id", "crop", "avg_yield_tph", "trend_rolling_3", "productivity_growth_pct"}.issubset(trends.columns)

    corr = pd.read_csv(outputs["rainfall_correlation_summary"])
    assert {"region_id", "rainfall_yield_correlation", "temperature_yield_correlation", "observations"}.issubset(corr.columns)

    impact = pd.read_csv(outputs["climate_impact_analysis"])
    assert {"climate_stress_index", "climate_stress_level", "estimated_productivity_impact_pct"}.issubset(impact.columns)
