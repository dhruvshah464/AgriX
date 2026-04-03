# Database Schema

## Entities

1. **regions**
   - `id` UUID PK
   - `name` VARCHAR(120)
   - `state` VARCHAR(120)
   - `country` VARCHAR(120)
   - `geometry_wkt` TEXT
   - `created_at`, `updated_at`

2. **farms**
   - `id` UUID PK
   - `farmer_name` VARCHAR(120)
   - `region_id` UUID FK -> regions.id
   - `area_hectares` FLOAT
   - `soil_type` VARCHAR(80)
   - `latitude`, `longitude` FLOAT
   - `created_at`, `updated_at`

3. **yield_predictions**
   - `id` UUID PK
   - `farm_id` UUID FK -> farms.id
   - `season` VARCHAR(40)
   - `model_name` VARCHAR(80)
   - `predicted_yield_tph` FLOAT
   - `confidence` FLOAT
   - `created_at`, `updated_at`

4. **climate_forecasts**
   - `id` UUID PK
   - `region_id` UUID FK -> regions.id
   - `forecast_date` DATE
   - `rainfall_mm`, `temperature_c`, `drought_index` FLOAT
   - `created_at`, `updated_at`

5. **ndvi_observations**
   - `id` UUID PK
   - `region_id` UUID FK -> regions.id
   - `observation_date` DATE
   - `source` VARCHAR(40)
   - `ndvi_mean`, `ndvi_min`, `ndvi_max` FLOAT
   - `created_at`, `updated_at`

6. **assistant_queries**
   - `id` UUID PK
   - `user_question` TEXT
   - `answer` TEXT
   - `source_docs` TEXT
   - `llm_provider` VARCHAR(40)
   - `created_at`, `updated_at`

## SQL DDL

See `docs/sql/schema.sql`.
