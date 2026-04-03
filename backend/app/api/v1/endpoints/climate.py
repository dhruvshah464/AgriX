from fastapi import APIRouter

from backend.app.schemas.climate import (
    ClimateForecastRequest,
    ClimateForecastResponse,
    ProductivityForecastRequest,
    ProductivityForecastResponse,
)
from backend.app.services.climate_service import ClimateService

router = APIRouter()
service = ClimateService()


@router.post("/forecast", response_model=ClimateForecastResponse)
def forecast(payload: ClimateForecastRequest) -> ClimateForecastResponse:
    return service.forecast(payload)


@router.post("/productivity-forecast", response_model=ProductivityForecastResponse)
def productivity_forecast(payload: ProductivityForecastRequest) -> ProductivityForecastResponse:
    return service.productivity_forecast(payload)
