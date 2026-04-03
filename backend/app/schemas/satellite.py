from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class NdviRequest(BaseModel):
    region_id: str
    red_band_path: str
    nir_band_path: str
    source: str = "sentinel-2"


class NdviResponse(BaseModel):
    region_id: str
    source: str
    observation_date: date
    ndvi_mean: float
    ndvi_min: float
    ndvi_max: float
