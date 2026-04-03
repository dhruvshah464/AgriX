from fastapi import APIRouter

from backend.app.api.v1.endpoints import assistant, climate, geospatial, health, prediction, satellite

api_router = APIRouter()
api_router.include_router(health.router, prefix="/system", tags=["system"])
api_router.include_router(prediction.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(climate.router, prefix="/climate", tags=["climate"])
api_router.include_router(satellite.router, prefix="/satellite", tags=["satellite"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["assistant"])
api_router.include_router(geospatial.router, prefix="/geospatial", tags=["geospatial"])
