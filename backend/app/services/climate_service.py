from __future__ import annotations

from backend.app.schemas.climate import (
    ClimateForecastPoint,
    ClimateForecastRequest,
    ClimateForecastResponse,
    ProductivityForecastPoint,
    ProductivityForecastRequest,
    ProductivityForecastResponse,
)
from climate_forecasting.arima_model.forecast import forecast_with_arima
from climate_forecasting.productivity_forecasting.system import forecast_crop_productivity
from climate_forecasting.prophet_model.forecast import forecast_with_prophet


class ClimateService:
    def forecast(self, payload: ClimateForecastRequest) -> ClimateForecastResponse:
        # Blend both model families for robust output.
        arima_points = forecast_with_arima(payload.region_id, payload.horizon_days)
        prophet_points = forecast_with_prophet(payload.region_id, payload.horizon_days)

        points: list[ClimateForecastPoint] = []
        for a, p in zip(arima_points, prophet_points, strict=False):
            points.append(
                ClimateForecastPoint(
                    date=a["date"],
                    rainfall_mm=round((a["rainfall_mm"] + p["rainfall_mm"]) / 2, 2),
                    temperature_c=round((a["temperature_c"] + p["temperature_c"]) / 2, 2),
                    drought_index=round((a["drought_index"] + p["drought_index"]) / 2, 3),
                )
            )

        return ClimateForecastResponse(region_id=payload.region_id, model_name="arima+prophet", points=points)

    def productivity_forecast(self, payload: ProductivityForecastRequest) -> ProductivityForecastResponse:
        rows = forecast_crop_productivity(region_id=payload.region_id, horizon_days=payload.horizon_days)
        points = [ProductivityForecastPoint(**row) for row in rows]
        return ProductivityForecastResponse(
            region_id=payload.region_id,
            model_name="arima+prophet_productivity",
            points=points,
        )
