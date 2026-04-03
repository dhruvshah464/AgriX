from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class ClimateForecastRequest(BaseModel):
    region_id: str
    horizon_days: int = 30


class ClimateForecastPoint(BaseModel):
    date: date
    rainfall_mm: float
    temperature_c: float
    drought_index: float


class ClimateForecastResponse(BaseModel):
    region_id: str
    model_name: str
    points: list[ClimateForecastPoint]


class ProductivityForecastRequest(BaseModel):
    region_id: str
    horizon_days: int = 30


class ProductivityForecastPoint(BaseModel):
    date: date
    rainfall_mm: float
    temperature_c: float
    productivity_arima: float
    productivity_prophet: float
    productivity_blended: float


class ProductivityForecastResponse(BaseModel):
    region_id: str
    model_name: str
    points: list[ProductivityForecastPoint]
