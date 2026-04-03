from __future__ import annotations

from datetime import UTC, datetime
import json
from urllib.parse import urlencode
from urllib.request import urlopen

try:
    import httpx
except Exception:  # pragma: no cover - optional dependency fallback
    httpx = None


class OpenWeatherClient:
    def __init__(self, api_key: str | None, base_url: str = "https://api.openweathermap.org/data/2.5"):
        self.api_key = api_key
        self.base_url = base_url

    def fetch_current_weather(self, lat: float, lon: float) -> dict:
        if not self.api_key:
            return {
                "timestamp": datetime.now(UTC).isoformat(),
                "temperature_c": 29.5,
                "rainfall_mm": 4.1,
                "humidity": 62,
            }

        params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": "metric"}
        if httpx is not None:
            response = httpx.get(f"{self.base_url}/weather", params=params, timeout=20.0)
            response.raise_for_status()
            data = response.json()
        else:
            query = urlencode(params)
            with urlopen(f"{self.base_url}/weather?{query}", timeout=20) as response:
                data = json.loads(response.read().decode("utf-8"))
        rain = data.get("rain", {}).get("1h", 0.0)
        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "temperature_c": data["main"]["temp"],
            "rainfall_mm": float(rain),
            "humidity": data["main"]["humidity"],
        }
