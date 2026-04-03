from __future__ import annotations

from climate_forecasting.arima_model.train import train as train_arima
from climate_forecasting.productivity_forecasting.system import train_productivity_models
from climate_forecasting.prophet_model.train import train as train_prophet
from data_pipeline.run_pipeline import run_full_pipeline
from ml_models.clustering.cluster import train as train_clusters
from ml_models.crop_classification.train import train as train_classifier
from ml_models.yield_prediction.train import train as train_yield
from rag_assistant.vector_db.index_manager import build_index


def run() -> None:
    print("[1/7] Running data pipeline...")
    run_full_pipeline()

    print("[2/7] Training yield prediction model...")
    print(train_yield())

    print("[3/7] Training crop suitability classifier...")
    print(train_classifier())

    print("[4/7] Training regional clustering model...")
    print(train_clusters())

    print("[5/7] Training climate forecasting models...")
    print(train_arima())
    print(train_prophet())

    print("[6/7] Training productivity forecasting models...")
    print(train_productivity_models())

    print("[7/7] Building RAG vector index...")
    print(build_index())


if __name__ == "__main__":
    run()
