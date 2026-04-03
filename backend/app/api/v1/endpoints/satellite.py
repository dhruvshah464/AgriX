from fastapi import APIRouter

from backend.app.schemas.satellite import NdviRequest, NdviResponse
from backend.app.services.satellite_service import SatelliteService

router = APIRouter()
service = SatelliteService()


@router.post("/ndvi", response_model=NdviResponse)
def ndvi(payload: NdviRequest) -> NdviResponse:
    return service.analyze_ndvi(payload)
