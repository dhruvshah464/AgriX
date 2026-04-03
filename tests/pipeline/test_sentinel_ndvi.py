from __future__ import annotations

import numpy as np

from satellite_analysis.ndvi_engine.sentinel_ndvi import classify_vegetation_health, compute_ndvi


def test_compute_ndvi_formula() -> None:
    red = np.array([[0.2, 0.3], [0.4, 0.1]], dtype="float32")
    nir = np.array([[0.6, 0.5], [0.4, 0.9]], dtype="float32")

    ndvi = compute_ndvi(red_band=red, nir_band=nir)
    expected = (nir - red) / (nir + red + 1e-10)
    assert np.allclose(ndvi, expected, atol=1e-6)
    assert float(ndvi.min()) >= -1.0
    assert float(ndvi.max()) <= 1.0


def test_vegetation_health_classification() -> None:
    ndvi = np.array([[-0.1, 0.2, 0.4, 0.6, 0.8]], dtype="float32")
    classes = classify_vegetation_health(ndvi)
    assert classes.tolist() == [[1, 2, 3, 4, 5]]
