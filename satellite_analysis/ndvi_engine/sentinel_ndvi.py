from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import geopandas as gpd
    import rasterio
    from rasterio.features import shapes
except Exception:  # pragma: no cover
    gpd = None
    rasterio = None
    shapes = None


def compute_ndvi(red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    """Compute NDVI from Sentinel-2 RED(B04) and NIR(B08) arrays."""
    red = red_band.astype("float32")
    nir = nir_band.astype("float32")
    denominator = nir + red + 1e-10
    ndvi = (nir - red) / denominator
    return np.clip(ndvi, -1.0, 1.0)


def classify_vegetation_health(ndvi: np.ndarray) -> np.ndarray:
    """
    Classify NDVI into vegetation health classes.
    1: Bare/Water (-1.00 to 0.10)
    2: Sparse (0.10 to 0.30)
    3: Moderate (0.30 to 0.50)
    4: Healthy (0.50 to 0.70)
    5: Very Healthy (0.70 to 1.00)
    """
    classes = np.zeros_like(ndvi, dtype="uint8")
    classes[(ndvi > -1.0) & (ndvi <= 0.10)] = 1
    classes[(ndvi > 0.10) & (ndvi <= 0.30)] = 2
    classes[(ndvi > 0.30) & (ndvi <= 0.50)] = 3
    classes[(ndvi > 0.50) & (ndvi <= 0.70)] = 4
    classes[(ndvi > 0.70)] = 5
    return classes


def _require_geospatial_deps() -> None:
    if rasterio is None or gpd is None or shapes is None:
        raise ImportError("Rasterio and GeoPandas are required for Sentinel-2 NDVI map export.")


def _vegetation_label(class_id: int) -> str:
    labels = {
        1: "bare_or_water",
        2: "sparse_vegetation",
        3: "moderate_vegetation",
        4: "healthy_vegetation",
        5: "very_healthy_vegetation",
    }
    return labels.get(class_id, "unknown")


def generate_vegetation_health_maps(
    red_band_path: str | Path,
    nir_band_path: str | Path,
    output_dir: str | Path,
    output_prefix: str = "sentinel2",
) -> dict[str, str | dict]:
    """
    Generate NDVI raster + vegetation-health vector map from Sentinel-2 bands.
    RED: Sentinel-2 B04
    NIR: Sentinel-2 B08
    """
    _require_geospatial_deps()

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    ndvi_raster_path = output_root / f"{output_prefix}_ndvi.tif"
    health_raster_path = output_root / f"{output_prefix}_vegetation_health.tif"
    health_vector_path = output_root / f"{output_prefix}_vegetation_health.geojson"
    health_summary_path = output_root / f"{output_prefix}_vegetation_health_summary.csv"

    with rasterio.open(red_band_path) as red_src, rasterio.open(nir_band_path) as nir_src:
        red_band = red_src.read(1).astype("float32")
        nir_band = nir_src.read(1).astype("float32")
        profile = red_src.profile.copy()
        transform = red_src.transform
        crs = red_src.crs

    ndvi = compute_ndvi(red_band=red_band, nir_band=nir_band)
    health_classes = classify_vegetation_health(ndvi)

    ndvi_profile = profile.copy()
    ndvi_profile.update(dtype=rasterio.float32, count=1, compress="lzw")
    with rasterio.open(ndvi_raster_path, "w", **ndvi_profile) as ndvi_dst:
        ndvi_dst.write(ndvi.astype("float32"), 1)

    class_profile = profile.copy()
    class_profile.update(dtype=rasterio.uint8, count=1, compress="lzw")
    with rasterio.open(health_raster_path, "w", **class_profile) as class_dst:
        class_dst.write(health_classes.astype("uint8"), 1)

    geom_value_iter = shapes(health_classes.astype("uint8"), transform=transform)
    features = [
        {"geometry": geom, "health_class": int(value), "health_label": _vegetation_label(int(value))}
        for geom, value in geom_value_iter
        if int(value) > 0
    ]
    gdf = gpd.GeoDataFrame(features, geometry="geometry", crs=crs)
    if gdf.empty:
        gdf = gpd.GeoDataFrame({"health_class": [], "health_label": []}, geometry=[], crs=crs)
    gdf.to_file(health_vector_path, driver="GeoJSON")

    class_counts = gdf["health_label"].value_counts().rename_axis("health_label").reset_index(name="polygon_count")
    class_counts.to_csv(health_summary_path, index=False)

    return {
        "ndvi_raster": str(ndvi_raster_path),
        "health_raster": str(health_raster_path),
        "health_vector_geojson": str(health_vector_path),
        "health_summary_csv": str(health_summary_path),
        "stats": {
            "ndvi_min": float(np.nanmin(ndvi)),
            "ndvi_max": float(np.nanmax(ndvi)),
            "ndvi_mean": float(np.nanmean(ndvi)),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute NDVI and vegetation health maps from Sentinel-2 bands.")
    parser.add_argument("--red-band", required=True, help="Path to Sentinel-2 RED band (B04) GeoTIFF.")
    parser.add_argument("--nir-band", required=True, help="Path to Sentinel-2 NIR band (B08) GeoTIFF.")
    parser.add_argument("--output-dir", required=True, help="Directory to save NDVI and health maps.")
    parser.add_argument("--prefix", default="sentinel2", help="Output filename prefix.")
    args = parser.parse_args()

    outputs = generate_vegetation_health_maps(
        red_band_path=args.red_band,
        nir_band_path=args.nir_band,
        output_dir=args.output_dir,
        output_prefix=args.prefix,
    )
    print(outputs)


if __name__ == "__main__":
    main()
