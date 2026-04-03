# ML Pipeline

## Yield Prediction
- Algorithms: RandomForest, GradientBoosting, XGBoost (when available)
- Target: `yield_tph`
- Features: rainfall, temperature, soil health, nutrient and stress indicators
- Artifact: `ml_models/artifacts/yield_model.joblib`

## Crop Suitability
- Algorithm: Logistic Regression classifier
- Target: `crop`
- Artifact: `ml_models/artifacts/crop_classifier.joblib`

## Region Clustering
- Algorithm: KMeans
- Features: rainfall, temperature, NDVI, soil fertility index
- Artifact: `ml_models/artifacts/region_cluster.joblib`

## Execution
- Full pipeline orchestration: `python scripts/train_all_models.py`
