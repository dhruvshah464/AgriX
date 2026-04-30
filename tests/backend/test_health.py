from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)

AUTH_HEADERS = {"Authorization": "Bearer fake-dev-token"}


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_yield_prediction_endpoint() -> None:
    response = client.post(
        "/api/v1/predictions/yield",
        headers=AUTH_HEADERS,
        json={
            "farm_id": "farm-001",
            "season": "kharif-2026",
            "rainfall_mm": 160,
            "temperature_c": 29,
            "soil_ph": 6.5,
            "nitrogen": 80,
            "phosphorus": 45,
            "potassium": 52,
        },
    )
    assert response.status_code == 200
    assert response.json()["predicted_yield_tph"] > 0
