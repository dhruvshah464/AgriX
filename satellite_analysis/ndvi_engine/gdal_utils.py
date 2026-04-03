from __future__ import annotations

try:
    from osgeo import gdal
except Exception:  # pragma: no cover
    gdal = None


def translate_to_geotiff(input_path: str, output_path: str) -> str:
    if gdal is None:
        return output_path
    gdal.Translate(output_path, input_path, format="GTiff")
    return output_path
