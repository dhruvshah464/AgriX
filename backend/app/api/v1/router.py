from fastapi import APIRouter, Depends
from backend.app.api.deps import get_current_user


from backend.app.api.v1.endpoints import assistant, climate, geospatial, health, prediction, satellite

api_router = APIRouter()
api_router.include_router(health.router, prefix="/system", tags=["system"])
api_router.include_router(prediction.router, prefix="/predictions", tags=["predictions"], dependencies=[Depends(get_current_user)])
api_router.include_router(climate.router, prefix="/climate", tags=["climate"], dependencies=[Depends(get_current_user)])
api_router.include_router(satellite.router, prefix="/satellite", tags=["satellite"], dependencies=[Depends(get_current_user)])
api_router.include_router(assistant.router, prefix="/assistant", tags=["assistant"], dependencies=[Depends(get_current_user)])
api_router.include_router(geospatial.router, prefix="/geospatial", tags=["geospatial"], dependencies=[Depends(get_current_user)])
