from __future__ import annotations

from datetime import date, timedelta


def forecast(region_id: str, horizon_days: int) -> list[dict]:
    baseline = []
    for i in range(horizon_days):
        baseline.append(
            {
                "region_id": region_id,
                "date": date.today() + timedelta(days=i + 1),
                "rainfall_mm": 55 + (i % 3) * 6,
                "temperature_c": 27 + (i % 4) * 0.5,
                "drought_index": 0.4,
            }
        )
    return baseline
