from __future__ import annotations

import argparse
from pathlib import Path

from climate_forecasting.productivity_forecasting.system import train_productivity_models


def main() -> None:
    parser = argparse.ArgumentParser(description="Train ARIMA + Prophet crop productivity forecasters.")
    parser.add_argument("--dataset-path", type=Path, default=Path("datasets/processed/productivity_history.csv"))
    parser.add_argument("--region-id", type=str, default="delhi-ncr")
    parser.add_argument(
        "--artifact-path",
        type=Path,
        default=Path("ml_models/artifacts/productivity_forecaster.joblib"),
    )
    args = parser.parse_args()

    result = train_productivity_models(
        dataset_path=args.dataset_path,
        region_id=args.region_id,
        artifact_path=args.artifact_path,
    )
    print(result)


if __name__ == "__main__":
    main()
