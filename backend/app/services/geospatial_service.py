from __future__ import annotations

from backend.app.schemas.geospatial import ProductivityMapResponse
from geospatial.geo_analysis.productivity import build_productivity_geojson


class GeospatialService:
    def productivity_map(self, region_id: str) -> ProductivityMapResponse:
        geojson = build_productivity_geojson(region_id)
        return ProductivityMapResponse(region_id=region_id, geojson=geojson)
