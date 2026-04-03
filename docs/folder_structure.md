# Folder Structure

```text
AgriX/
  backend/                  # FastAPI app, domain services, schemas, ORM models
  data_pipeline/            # Ingestion, preprocessing, feature engineering
  ml_models/                # Training and inference pipelines + artifacts
  climate_forecasting/      # ARIMA and Prophet models
  satellite_analysis/       # NDVI compute and satellite loaders
  rag_assistant/            # Embeddings, vector index, assistant orchestration
  geospatial/               # Productivity geojson and map support
  dashboards/               # KPI analytics + Power BI exports
  frontend/react_app/       # React + Tailwind + Mapbox client
  datasets/                 # Raw/processed/external data lake
  notebooks/eda/            # Exploratory notebooks
  docker/                   # Dockerfiles and compose stack
  docs/                     # Architecture and design documentation
  scripts/                  # Operational scripts
  tests/                    # Backend, ML, and pipeline tests
```
