from __future__ import annotations

from pydantic import BaseModel


class ProductivityMapRequest(BaseModel):
    region_id: str


class ProductivityMapResponse(BaseModel):
    region_id: str
    geojson: dict
