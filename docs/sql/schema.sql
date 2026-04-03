CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS regions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(120) NOT NULL,
  state VARCHAR(120) NOT NULL,
  country VARCHAR(120) NOT NULL DEFAULT 'India',
  geometry_wkt TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS farms (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  farmer_name VARCHAR(120) NOT NULL,
  region_id UUID NOT NULL REFERENCES regions(id),
  area_hectares FLOAT NOT NULL,
  soil_type VARCHAR(80),
  latitude FLOAT NOT NULL,
  longitude FLOAT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS yield_predictions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  farm_id UUID NOT NULL REFERENCES farms(id),
  season VARCHAR(40) NOT NULL,
  model_name VARCHAR(80) NOT NULL,
  predicted_yield_tph FLOAT NOT NULL,
  confidence FLOAT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS climate_forecasts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  region_id UUID NOT NULL REFERENCES regions(id),
  forecast_date DATE NOT NULL,
  rainfall_mm FLOAT NOT NULL,
  temperature_c FLOAT NOT NULL,
  drought_index FLOAT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ndvi_observations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  region_id UUID NOT NULL REFERENCES regions(id),
  observation_date DATE NOT NULL,
  source VARCHAR(40) NOT NULL,
  ndvi_mean FLOAT NOT NULL,
  ndvi_min FLOAT NOT NULL,
  ndvi_max FLOAT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS assistant_queries (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_question TEXT NOT NULL,
  answer TEXT NOT NULL,
  source_docs TEXT,
  llm_provider VARCHAR(40) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
