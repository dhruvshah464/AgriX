# AgriX Architecture

## 1) System Overview

AgriX is organized as a modular platform with service boundaries aligned to agricultural intelligence capabilities.

- **Data Engineering Layer**: ingestion, cleaning, feature engineering, and curated training/export datasets.
- **ML & Forecast Layer**: yield regression, crop suitability classification, region clustering, ARIMA/Prophet forecasting.
- **Geospatial & Remote Sensing Layer**: NDVI computation, change detection, productivity map generation.
- **RAG Intelligence Layer**: document embedding, FAISS retrieval, LLM answer generation.
- **API Layer**: FastAPI endpoints exposing predictions, insights, NDVI, forecasting, assistant.
- **Frontend Layer**: React + Tailwind + Mapbox dashboards for interactive exploration.
- **Infra Layer**: Docker microservices, CI pipeline, PostgreSQL persistence, export pipelines.

## 2) Logical Components

1. `data_pipeline/` produces cleaned and feature-rich datasets.
2. `ml_models/` trains and serves model artifacts.
3. `climate_forecasting/` forecasts weather-driven climate signals.
4. `satellite_analysis/` computes NDVI and vegetation change.
5. `rag_assistant/` enables agronomy Q&A with retrieval.
6. `geospatial/` produces map-ready GeoJSON.
7. `backend/` orchestrates all capabilities through APIs.
8. `frontend/react_app/` renders dashboards and geospatial views.

## 3) Deployment Topology

- `api` FastAPI service
- `ml_worker` periodic trainer/batch processor
- `rag_indexer` vector index builder
- `frontend` static app served through Nginx
- `postgres` relational data store
