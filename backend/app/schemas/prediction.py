from __future__ import annotations

from pydantic import BaseModel, Field


class YieldPredictionRequest(BaseModel):
    farm_id: str
    season: str = Field(examples=["kharif-2026"])
    rainfall_mm: float
    temperature_c: float
    soil_ph: float
    nitrogen: float
    phosphorus: float
    potassium: float


class YieldPredictionResponse(BaseModel):
    farm_id: str
    season: str
    predicted_yield_tph: float
    model_name: str
    confidence: float


class CropSuitabilityRequest(BaseModel):
    rainfall_mm: float
    temperature_c: float
    soil_ph: float
    nitrogen: float
    phosphorus: float
    potassium: float


class CropSuitabilityResponse(BaseModel):
    recommended_crop: str
    confidence: float


class CropRecommendationRequest(BaseModel):
    rainfall_mm: float
    temperature_c: float
    soil_ph: float
    nitrogen: float
    phosphorus: float
    potassium: float


class CropRecommendationResponse(BaseModel):
    recommended_crop: str
    confidence: float


class RegionClusterRequest(BaseModel):
    region_id: str
    avg_rainfall_mm: float
    avg_temperature_c: float
    avg_ndvi: float
    soil_fertility_index: float


class RegionClusterResponse(BaseModel):
    region_id: str
    cluster_id: int
