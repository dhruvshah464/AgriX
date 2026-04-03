from ml_models.crop_classification.infer import infer_crop_suitability
from ml_models.yield_prediction.predict import predict_yield


def test_yield_predictor_fallback() -> None:
    prediction, confidence, model = predict_yield(
        {
            "rainfall_mm": 150,
            "temperature_c": 28,
            "soil_ph": 6.6,
            "nitrogen": 75,
            "phosphorus": 42,
            "potassium": 49,
        }
    )
    assert prediction > 0
    assert 0 <= confidence <= 1
    assert isinstance(model, str)


def test_crop_classifier_fallback() -> None:
    crop, confidence = infer_crop_suitability(
        {
            "rainfall_mm": 160,
            "temperature_c": 29,
            "soil_ph": 6.4,
            "nitrogen": 80,
            "phosphorus": 45,
            "potassium": 50,
        }
    )
    assert isinstance(crop, str)
    assert 0 <= confidence <= 1
