# Satellite Analysis

## Data Sources
- Sentinel-2
- Landsat

## NDVI Engine
- Formula: `(NIR - Red) / (NIR + Red + epsilon)`
- Output: min, max, mean NDVI
- Module: `satellite_analysis/ndvi_engine/compute_ndvi.py`

## Change Detection
- Compares old/new NDVI means to classify trend
- Module: `satellite_analysis/ndvi_engine/change_detection.py`

## Catalog Loader
- Extracts scene metadata and provider tags
- Module: `satellite_analysis/satellite_data_loader/loader.py`
