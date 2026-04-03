from __future__ import annotations

from satellite_analysis.ndvi_engine.compute_ndvi import compute_ndvi_stats


def detect_change(old_red: str, old_nir: str, new_red: str, new_nir: str) -> dict:
    old_stats = compute_ndvi_stats(old_red, old_nir)
    new_stats = compute_ndvi_stats(new_red, new_nir)
    delta = new_stats["mean"] - old_stats["mean"]

    return {
        "old_mean": old_stats["mean"],
        "new_mean": new_stats["mean"],
        "delta": round(delta, 4),
        "trend": "improving" if delta > 0 else "declining",
    }
