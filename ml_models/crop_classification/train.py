from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from ml_models.common.io import save_artifact


FEATURES = ["rainfall_mm", "temperature_c", "soil_ph", "nitrogen", "phosphorus", "potassium"]
TARGET = "crop"


def train(dataset_path: Path = Path("datasets/processed/training_agri.csv"), artifact_path: Path = Path("ml_models/artifacts/crop_classifier.joblib")) -> dict:
    frame = pd.read_csv(dataset_path).dropna(subset=[TARGET])
    X = frame[[f for f in FEATURES if f in frame.columns]]
    y = frame[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    accuracy = float(accuracy_score(y_test, preds))

    payload = {
        "model": model,
        "features": list(X.columns),
        "classes": list(model.classes_),
        "model_name": "logistic_regression",
        "metrics": {"accuracy": accuracy},
    }
    save_artifact(payload, artifact_path)
    return payload["metrics"]


if __name__ == "__main__":
    print(train())
