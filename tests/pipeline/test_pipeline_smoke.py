import pandas as pd

from data_pipeline.feature_engineering.build_features import build
from data_pipeline.preprocessing.clean_data import clean_agri_frame


def test_pipeline_feature_building() -> None:
    frame = pd.DataFrame(
        [
            {
                "rainfall_mm": 120,
                "temperature_c": 30,
                "soil_ph": 6.5,
                "nitrogen": 70,
                "phosphorus": 40,
                "potassium": 45,
                "yield_tph": 3.5,
                "crop": "Rice",
            }
        ]
    )
    cleaned = clean_agri_frame(frame)
    featured = build(cleaned)
    assert "nutrient_score" in featured.columns
    assert "water_stress_index" in featured.columns
