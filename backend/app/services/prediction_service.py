from __future__ import annotations

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
from ml_models.clustering.infer import assign_cluster
from ml_models.crop_classification.infer import infer_crop_suitability
from ml_models.yield_prediction.predict import predict_yield


class PredictionService:
    def predict_yield(self, payload: YieldPredictionRequest) -> YieldPredictionResponse:
        predicted, confidence, model_name = predict_yield(payload.model_dump())
        return YieldPredictionResponse(
            farm_id=payload.farm_id,
            season=payload.season,
            predicted_yield_tph=predicted,
            model_name=model_name,
            confidence=confidence,
        )

    def crop_suitability(self, payload: CropSuitabilityRequest) -> CropSuitabilityResponse:
        crop, confidence = infer_crop_suitability(payload.model_dump())
        return CropSuitabilityResponse(recommended_crop=crop, confidence=confidence)

    def crop_recommendation(self, payload: CropRecommendationRequest) -> CropRecommendationResponse:
        crop, confidence = infer_crop_suitability(payload.model_dump())
        return CropRecommendationResponse(recommended_crop=crop, confidence=confidence)

    def cluster_region(self, payload: RegionClusterRequest) -> RegionClusterResponse:
        cluster_id = assign_cluster(payload.model_dump())
        return RegionClusterResponse(region_id=payload.region_id, cluster_id=cluster_id)
