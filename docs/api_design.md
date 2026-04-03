# Backend API Design

Base URL: `/api/v1`

## System
- `GET /system/health`

## Predictions
- `POST /predictions/yield`
  - Inputs: farm/soil/weather features
  - Output: predicted yield, model_name, confidence
- `POST /predictions/recommendation`
  - Inputs: agro-climatic + soil nutrient features
  - Output: recommended crop + confidence
- `POST /predictions/suitability`
  - Inputs: agro-climatic features
  - Output: recommended crop + confidence
- `POST /predictions/cluster`
  - Inputs: regional aggregate features
  - Output: cluster_id

## Climate
- `POST /climate/forecast`
  - Inputs: region_id, horizon_days
  - Output: blended ARIMA+Prophet forecast points

## Satellite
- `POST /satellite/ndvi`
  - Inputs: region_id, red band path, NIR band path
  - Output: ndvi_min/mean/max

## Assistant
- `POST /assistant/query`
  - Inputs: question text
  - Output: answer + retrieved source snippets

## Geospatial
- `POST /geospatial/productivity-map`
  - Inputs: region_id
  - Output: GeoJSON feature collection
