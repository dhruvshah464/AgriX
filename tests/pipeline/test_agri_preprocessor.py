from __future__ import annotations

import pandas as pd

from data_pipeline.preprocessing.agri_preprocessor import AgriculturalPreprocessor


def test_agri_preprocessor_handles_requested_tasks() -> None:
    df = pd.DataFrame(
        [
            {"region_id": "r1", "season": "kharif", "rainfall_mm": 180, "temperature_c": 31, "soil_type": "Loam"},
            {"region_id": "r1", "season": "kharif", "rainfall_mm": None, "temperature_c": 30, "soil_type": "Clay"},
            {"region_id": "r1", "season": "rabi", "rainfall_mm": 60, "temperature_c": None, "soil_type": None},
            {"region_id": "r2", "season": "rabi", "rainfall_mm": 72, "temperature_c": 21, "soil_type": "Sandy"},
        ]
    )

    processed = AgriculturalPreprocessor().preprocess(df)

    # Missing values handled.
    assert processed["rainfall_mm"].isna().sum() == 0
    assert processed["temperature_c"].isna().sum() == 0
    assert processed["soil_type"].isna().sum() == 0

    # Rainfall and temperature normalized.
    assert "rainfall_mm_norm" in processed.columns
    assert "temperature_c_norm" in processed.columns
    assert processed["rainfall_mm_norm"].between(0, 1).all()
    assert processed["temperature_c_norm"].between(0, 1).all()

    # Soil type encoded.
    assert "soil_type_code" in processed.columns
    dummy_cols = [c for c in processed.columns if c.startswith("soil_type_") and c != "soil_type_code"]
    assert len(dummy_cols) >= 2

    # Seasonal rainfall average generated.
    assert "seasonal_rainfall_avg" in processed.columns
    grouped_expected = processed.groupby(["region_id", "season"])["rainfall_mm"].transform("mean").round(3)
    assert grouped_expected.equals(processed["seasonal_rainfall_avg"])
