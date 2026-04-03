# Dashboard Architecture

## Interactive Web Dashboards
- Recharts-based trend and climate visuals
- KPI cards and assistant insights
- Geospatial overlay through Mapbox

## BI Exports
- `dashboards/powerbi_exports/export_pipeline.py`
- Exports:
  - `yield_summary.csv`
  - `kpis.csv`
  - `training_agri.parquet`

These outputs are Power BI-compatible and can be refreshed by scheduled batch jobs.
