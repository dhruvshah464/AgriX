from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_crop_yield_prediction_endpoint() -> None:
    response = client.post(
        "/api/v1/predictions/yield",
        json={
            "farm_id": "farm-100",
            "season": "kharif-2026",
            "rainfall_mm": 155,
            "temperature_c": 28.2,
            "soil_ph": 6.6,
            "nitrogen": 78,
            "phosphorus": 44,
            "potassium": 50,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_yield_tph"] > 0
    assert isinstance(body["model_name"], str)


def test_crop_recommendation_endpoint() -> None:
    response = client.post(
        "/api/v1/predictions/recommendation",
        json={
            "rainfall_mm": 180,
            "temperature_c": 29.5,
            "soil_ph": 6.4,
            "nitrogen": 85,
            "phosphorus": 46,
            "potassium": 54,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["recommended_crop"], str)
    assert 0 <= body["confidence"] <= 1


def test_ndvi_analysis_endpoint(monkeypatch) -> None:
    def _mock_stats(_: str, __: str) -> dict[str, float]:
        return {"mean": 0.58, "min": 0.22, "max": 0.83}

    monkeypatch.setattr("backend.app.services.satellite_service.compute_ndvi_stats", _mock_stats)
    response = client.post(
        "/api/v1/satellite/ndvi",
        json={
            "region_id": "delhi-ncr",
            "red_band_path": "/tmp/red.tif",
            "nir_band_path": "/tmp/nir.tif",
            "source": "sentinel-2",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["ndvi_mean"] == 0.58
    assert body["ndvi_min"] == 0.22
    assert body["ndvi_max"] == 0.83


def test_climate_forecast_endpoint() -> None:
    response = client.post(
        "/api/v1/climate/forecast",
        json={"region_id": "delhi-ncr", "horizon_days": 5},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["model_name"] == "arima+prophet"
    assert len(body["points"]) == 5
    assert "rainfall_mm" in body["points"][0]
    assert "temperature_c" in body["points"][0]


def test_ai_assistant_query_endpoint() -> None:
    response = client.post(
        "/api/v1/assistant/query",
        json={"query": "How to improve wheat yield in low rainfall conditions?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["answer"], str)
    assert isinstance(body["sources"], list)
