from fastapi import APIRouter

from backend.app.schemas.prediction import (
    CropRecommendationRequest,
    CropRecommendationResponse,
    CropSuitabilityRequest,
    CropSuitabilityResponse,
    RegionClusterRequest,
    RegionClusterResponse,
    YieldPredictionRequest,
    YieldPredictionResponse,
)
from backend.app.services.prediction_service import PredictionService

router = APIRouter()
service = PredictionService()


@router.post("/yield", response_model=YieldPredictionResponse)
def predict_yield(payload: YieldPredictionRequest) -> YieldPredictionResponse:
    return service.predict_yield(payload)


@router.post("/suitability", response_model=CropSuitabilityResponse)
def crop_suitability(payload: CropSuitabilityRequest) -> CropSuitabilityResponse:
    return service.crop_suitability(payload)


@router.post("/recommendation", response_model=CropRecommendationResponse)
def crop_recommendation(payload: CropRecommendationRequest) -> CropRecommendationResponse:
    return service.crop_recommendation(payload)


@router.post("/cluster", response_model=RegionClusterResponse)
def cluster_region(payload: RegionClusterRequest) -> RegionClusterResponse:
    return service.cluster_region(payload)
