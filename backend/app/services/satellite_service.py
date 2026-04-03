from __future__ import annotations

from datetime import date

from backend.app.schemas.satellite import NdviRequest, NdviResponse
from satellite_analysis.ndvi_engine.compute_ndvi import compute_ndvi_stats


class SatelliteService:
    def analyze_ndvi(self, payload: NdviRequest) -> NdviResponse:
        stats = compute_ndvi_stats(payload.red_band_path, payload.nir_band_path)
        return NdviResponse(
            region_id=payload.region_id,
            source=payload.source,
            observation_date=date.today(),
            ndvi_mean=stats["mean"],
            ndvi_min=stats["min"],
            ndvi_max=stats["max"],
        )
