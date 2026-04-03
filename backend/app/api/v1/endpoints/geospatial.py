from fastapi import APIRouter

from backend.app.schemas.geospatial import ProductivityMapRequest, ProductivityMapResponse
from backend.app.services.geospatial_service import GeospatialService

router = APIRouter()
service = GeospatialService()


@router.post("/productivity-map", response_model=ProductivityMapResponse)
def productivity_map(payload: ProductivityMapRequest) -> ProductivityMapResponse:
    return service.productivity_map(payload.region_id)
