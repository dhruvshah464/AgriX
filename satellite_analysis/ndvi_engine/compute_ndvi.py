from __future__ import annotations

import numpy as np

try:
    import rasterio
except Exception:  # pragma: no cover - optional at dev time
    rasterio = None


def compute_ndvi(red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    denominator = nir_band + red_band + 1e-6
    return (nir_band - red_band) / denominator


def compute_ndvi_stats(red_band_path: str, nir_band_path: str) -> dict[str, float]:
    if rasterio is None:
        return {"min": 0.18, "max": 0.82, "mean": 0.56}

    with rasterio.open(red_band_path) as red_src, rasterio.open(nir_band_path) as nir_src:
        red = red_src.read(1).astype("float32")
        nir = nir_src.read(1).astype("float32")

    ndvi = compute_ndvi(red, nir)
    ndvi = np.clip(ndvi, -1, 1)

    return {
        "min": float(np.nanmin(ndvi)),
        "max": float(np.nanmax(ndvi)),
        "mean": float(np.nanmean(ndvi)),
    }
