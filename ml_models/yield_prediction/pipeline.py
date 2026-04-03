from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

from ml_models.common.io import save_artifact


class SimpleGradientBoostingRegressor(BaseEstimator, RegressorMixin):
    """Lightweight gradient boosting regressor using decision trees as weak learners."""

    def __init__(
        self,
        n_estimators: int = 200,
        learning_rate: float = 0.05,
        max_depth: int = 3,
        random_state: int = 42,
    ):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.random_state = random_state

    def fit(self, x: np.ndarray, y: np.ndarray):
        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)
        if x_arr.ndim != 2:
            raise ValueError("Input features must be 2D for gradient boosting.")

        self.base_prediction_ = float(np.mean(y_arr))
        self.trees_: list[DecisionTreeRegressor] = []
        prediction = np.full(shape=y_arr.shape, fill_value=self.base_prediction_, dtype=float)

        for idx in range(self.n_estimators):
            residual = y_arr - prediction
            tree = DecisionTreeRegressor(max_depth=self.max_depth, random_state=self.random_state + idx)
            tree.fit(x_arr, residual)
            update = tree.predict(x_arr)
            prediction += self.learning_rate * update
            self.trees_.append(tree)

        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        x_arr = np.asarray(x, dtype=float)
        prediction = np.full(shape=(x_arr.shape[0],), fill_value=self.base_prediction_, dtype=float)
        for tree in self.trees_:
            prediction += self.learning_rate * tree.predict(x_arr)
        return prediction


@dataclass(slots=True)
class YieldPipelineConfig:
    feature_columns: list[str]
    target_column: str = "yield_tph"
    test_size: float = 0.2
    random_state: int = 42
    cv_folds: int = 5


def _build_preprocessor(feature_columns: list[str]) -> ColumnTransformer:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    return ColumnTransformer(
        transformers=[("num", numeric_transformer, feature_columns)],
        remainder="drop",
    )


def _build_model_pipelines(feature_columns: list[str], random_state: int) -> dict[str, Pipeline]:
    base_preprocessor = _build_preprocessor(feature_columns)

    return {
        "linear_regression": Pipeline(
            steps=[
                ("preprocessor", base_preprocessor),
                ("model", LinearRegression()),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("preprocessor", base_preprocessor),
                ("model", RandomForestRegressor(n_estimators=300, random_state=random_state)),
            ]
        ),
        "gradient_boosting": Pipeline(
            steps=[
                ("preprocessor", base_preprocessor),
                ("model", SimpleGradientBoostingRegressor(random_state=random_state)),
            ]
        ),
    }


class CropYieldMLPipeline:
    def __init__(self, config: YieldPipelineConfig):
        self.config = config

    def _prepare_frame(self, frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        if self.config.target_column not in frame.columns:
            raise ValueError(f"Target column '{self.config.target_column}' not found in dataset.")

        available_features = [c for c in self.config.feature_columns if c in frame.columns]
        if not available_features:
            raise ValueError("None of the configured feature columns are present in dataset.")

        data = frame[available_features + [self.config.target_column]].copy()
        for col in available_features + [self.config.target_column]:
            data[col] = pd.to_numeric(data[col], errors="coerce")
        data = data.dropna(subset=[self.config.target_column]).reset_index(drop=True)

        if len(data) < 3:
            raise ValueError("At least 3 rows are required to train and evaluate the yield models.")

        x = data[available_features]
        y = data[self.config.target_column]
        return x, y

    @staticmethod
    def _evaluate(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
        rmse = mean_squared_error(y_true, y_pred) ** 0.5
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        return {
            "rmse": float(rmse),
            "mae": float(mae),
            "r2": float(r2),
        }

    def train(self, frame: pd.DataFrame) -> dict:
        x, y = self._prepare_frame(frame)
        feature_columns = list(x.columns)

        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=self.config.test_size,
            random_state=self.config.random_state,
        )

        models = _build_model_pipelines(feature_columns=feature_columns, random_state=self.config.random_state)

        leaderboard: dict[str, dict] = {}
        fitted_models: dict[str, Pipeline] = {}

        n_train = len(x_train)
        cv_folds = min(self.config.cv_folds, n_train)
        can_cv = cv_folds >= 2

        for model_name, pipeline in models.items():
            cv_metrics: dict[str, float] = {}
            if can_cv:
                cv = KFold(n_splits=cv_folds, shuffle=True, random_state=self.config.random_state)
                scores = cross_validate(
                    pipeline,
                    x_train,
                    y_train,
                    cv=cv,
                    scoring={
                        "rmse": "neg_root_mean_squared_error",
                        "mae": "neg_mean_absolute_error",
                        "r2": "r2",
                    },
                    n_jobs=None,
                )
                cv_metrics = {
                    "cv_rmse_mean": float(-scores["test_rmse"].mean()),
                    "cv_rmse_std": float(scores["test_rmse"].std()),
                    "cv_mae_mean": float(-scores["test_mae"].mean()),
                    "cv_r2_mean": float(scores["test_r2"].mean()),
                }

            pipeline.fit(x_train, y_train)
            y_pred = pipeline.predict(x_test)
            test_metrics = self._evaluate(y_true=y_test, y_pred=y_pred)

            leaderboard[model_name] = {
                **test_metrics,
                **cv_metrics,
            }
            fitted_models[model_name] = pipeline

        # Select the best model primarily by cross-validation RMSE if available.
        if can_cv:
            best_model_name = min(leaderboard.keys(), key=lambda name: leaderboard[name]["cv_rmse_mean"])
        else:
            best_model_name = min(leaderboard.keys(), key=lambda name: leaderboard[name]["rmse"])

        best_model = fitted_models[best_model_name]
        best_metrics = leaderboard[best_model_name]

        return {
            "models": fitted_models,
            "features": feature_columns,
            "leaderboard": leaderboard,
            "best_model_name": best_model_name,
            "best_model": best_model,
            "best_metrics": best_metrics,
        }


def train_and_persist(
    dataset_path: Path,
    best_artifact_path: Path,
    bundle_artifact_path: Path,
    config: YieldPipelineConfig,
) -> dict:
    frame = pd.read_csv(dataset_path)
    trainer = CropYieldMLPipeline(config=config)
    results = trainer.train(frame)

    bundle_payload = {
        "models": results["models"],
        "features": results["features"],
        "leaderboard": results["leaderboard"],
        "best_model_name": results["best_model_name"],
        "target": config.target_column,
        "config": {
            "feature_columns": config.feature_columns,
            "target_column": config.target_column,
            "test_size": config.test_size,
            "random_state": config.random_state,
            "cv_folds": config.cv_folds,
        },
    }
    save_artifact(bundle_payload, bundle_artifact_path)

    best_payload = {
        "model": results["best_model"],
        "features": results["features"],
        "model_name": results["best_model_name"],
        "metrics": results["best_metrics"],
        "leaderboard": results["leaderboard"],
    }
    save_artifact(best_payload, best_artifact_path)

    return {
        "model_name": results["best_model_name"],
        "metrics": results["best_metrics"],
        "leaderboard": results["leaderboard"],
        "best_artifact_path": str(best_artifact_path),
        "bundle_artifact_path": str(bundle_artifact_path),
    }
