from __future__ import annotations

import argparse
from pathlib import Path

from climate_forecasting.productivity_forecasting.system import forecast_crop_productivity


def main() -> None:
    parser = argparse.ArgumentParser(description="Forecast crop productivity with ARIMA + Prophet.")
    parser.add_argument("--region-id", type=str, default="delhi-ncr")
    parser.add_argument("--horizon-days", type=int, default=30)
    parser.add_argument(
        "--artifact-path",
        type=Path,
        default=Path("ml_models/artifacts/productivity_forecaster.joblib"),
    )
    args = parser.parse_args()

    points = forecast_crop_productivity(
        region_id=args.region_id,
        horizon_days=args.horizon_days,
        artifact_path=args.artifact_path,
    )
    print(points)


if __name__ == "__main__":
    main()
