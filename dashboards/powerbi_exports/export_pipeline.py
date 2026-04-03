from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from dashboards.analytics.dashboard_builder import (
    build_climate_impact_dashboard,
    build_productivity_trends_dashboard,
    build_rainfall_correlation_dashboard,
)
from dashboards.analytics.metrics_service import compute_kpis_from_frame


SEASON_MONTH_MAP = {
    "kharif": 7,
    "rabi": 1,
    "zaid": 4,
}


def _pick_crop_source(source_path: Path | None = None) -> Path:
    candidates = [source_path] if source_path else []
    candidates.extend([Path("datasets/processed/training_agri.csv"), Path("datasets/raw/crop_yield.csv")])
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    raise FileNotFoundError("No crop dataset found. Expected one of datasets/processed/training_agri.csv or datasets/raw/crop_yield.csv.")


def _load_crop_data(source_path: Path | None = None) -> pd.DataFrame:
    frame = pd.read_csv(_pick_crop_source(source_path))
    if "yield_tph" not in frame.columns:
        raise ValueError("Crop dataset must include 'yield_tph' column.")
    if "region_id" not in frame.columns:
        frame["region_id"] = "unknown-region"
    if "crop" not in frame.columns:
        frame["crop"] = "unknown-crop"

    frame["yield_tph"] = pd.to_numeric(frame["yield_tph"], errors="coerce")
    frame["rainfall_mm"] = pd.to_numeric(frame.get("rainfall_mm", pd.Series([None] * len(frame))), errors="coerce")
    frame["temperature_c"] = pd.to_numeric(frame.get("temperature_c", pd.Series([None] * len(frame))), errors="coerce")

    if "date" in frame.columns:
        frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    else:
        years = pd.to_numeric(frame.get("year", pd.Series([pd.Timestamp.today().year] * len(frame))), errors="coerce").fillna(pd.Timestamp.today().year).astype(int)
        season = frame.get("season", pd.Series(["kharif"] * len(frame))).astype(str).str.lower()
        months = season.map(SEASON_MONTH_MAP).fillna(6).astype(int)
        frame["date"] = pd.to_datetime({"year": years, "month": months, "day": 1})

    frame = frame.dropna(subset=["yield_tph", "date"]).reset_index(drop=True)
    return frame


def _load_climate_data(climate_path: Path) -> pd.DataFrame:
    if not climate_path.exists():
        return pd.DataFrame(columns=["date", "region_id", "rainfall_mm", "temperature_c"])

    climate = pd.read_csv(climate_path)
    if "date" not in climate.columns:
        return pd.DataFrame(columns=["date", "region_id", "rainfall_mm", "temperature_c"])

    climate["date"] = pd.to_datetime(climate["date"], errors="coerce")
    climate["rainfall_mm"] = pd.to_numeric(climate.get("rainfall_mm"), errors="coerce")
    climate["temperature_c"] = pd.to_numeric(climate.get("temperature_c"), errors="coerce")
    if "region_id" not in climate.columns:
        climate["region_id"] = "unknown-region"
    return climate.dropna(subset=["date"]).reset_index(drop=True)


def _load_productivity_history(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["date", "region_id", "yield_tph"])
    frame = pd.read_csv(path)
    if "yield_tph" not in frame.columns and "productivity_index" in frame.columns:
        frame["yield_tph"] = pd.to_numeric(frame["productivity_index"], errors="coerce")
    frame["date"] = pd.to_datetime(frame.get("date"), errors="coerce")
    if "region_id" not in frame.columns:
        frame["region_id"] = "unknown-region"
    return frame.dropna(subset=["date", "yield_tph"]).reset_index(drop=True)


def _build_crop_productivity_trends(crop_df: pd.DataFrame, productivity_history_df: pd.DataFrame) -> pd.DataFrame:
    crop_trends = (
        crop_df.groupby(["date", "region_id", "crop"], as_index=False)["yield_tph"]
        .mean()
        .rename(columns={"yield_tph": "avg_yield_tph"})
    )

    if not productivity_history_df.empty:
        hist = (
            productivity_history_df.groupby(["date", "region_id"], as_index=False)["yield_tph"]
            .mean()
            .rename(columns={"yield_tph": "avg_yield_tph"})
        )
        hist["crop"] = "all"
        combined = pd.concat([crop_trends, hist], ignore_index=True)
        trends = (
            combined.groupby(["date", "region_id", "crop"], as_index=False)["avg_yield_tph"]
            .mean()
            .sort_values(["region_id", "crop", "date"])
            .reset_index(drop=True)
        )
    else:
        trends = crop_trends.sort_values(["region_id", "crop", "date"]).reset_index(drop=True)

    trends["trend_rolling_3"] = (
        trends.groupby(["region_id", "crop"], dropna=False)["avg_yield_tph"]
        .transform(lambda s: s.rolling(window=3, min_periods=1).mean())
        .round(3)
    )
    trends["productivity_growth_pct"] = (
        trends.groupby(["region_id", "crop"], dropna=False)["avg_yield_tph"].pct_change().fillna(0.0) * 100
    ).round(3)
    return trends


def _build_rainfall_correlation(crop_df: pd.DataFrame, climate_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    observations = crop_df.loc[:, ["date", "region_id", "crop", "yield_tph", "rainfall_mm", "temperature_c"]].copy()

    if not climate_df.empty:
        climate_slice = climate_df.loc[:, ["date", "region_id", "rainfall_mm", "temperature_c"]].rename(
            columns={"rainfall_mm": "rainfall_mm_climate", "temperature_c": "temperature_c_climate"}
        )
        observations = observations.merge(climate_slice, on=["date", "region_id"], how="left")
        observations["rainfall_mm"] = observations["rainfall_mm"].fillna(observations["rainfall_mm_climate"])
        observations["temperature_c"] = observations["temperature_c"].fillna(observations["temperature_c_climate"])
        observations = observations.drop(columns=["rainfall_mm_climate", "temperature_c_climate"])

    observations["rainfall_mm"] = pd.to_numeric(observations["rainfall_mm"], errors="coerce")
    observations["temperature_c"] = pd.to_numeric(observations["temperature_c"], errors="coerce")
    observations["yield_tph"] = pd.to_numeric(observations["yield_tph"], errors="coerce")

    observations["rainfall_mm"] = observations.groupby("region_id")["rainfall_mm"].transform(lambda s: s.fillna(s.mean()))
    observations["temperature_c"] = observations.groupby("region_id")["temperature_c"].transform(lambda s: s.fillna(s.mean()))
    observations = observations.dropna(subset=["rainfall_mm", "yield_tph"]).reset_index(drop=True)

    corr_rows = []
    for region_id, grp in observations.groupby("region_id"):
        corr_rows.append(
            {
                "region_id": region_id,
                "rainfall_yield_correlation": float(grp["rainfall_mm"].corr(grp["yield_tph"])) if len(grp) > 1 else 0.0,
                "temperature_yield_correlation": float(grp["temperature_c"].corr(grp["yield_tph"])) if len(grp) > 1 else 0.0,
                "observations": int(len(grp)),
            }
        )
    correlation = pd.DataFrame(corr_rows)

    global_row = pd.DataFrame(
        [
            {
                "region_id": "all-regions",
                "rainfall_yield_correlation": float(observations["rainfall_mm"].corr(observations["yield_tph"])) if len(observations) > 1 else 0.0,
                "temperature_yield_correlation": float(observations["temperature_c"].corr(observations["yield_tph"])) if len(observations) > 1 else 0.0,
                "observations": int(len(observations)),
            }
        ]
    )
    correlation = pd.concat([correlation, global_row], ignore_index=True)
    correlation[["rainfall_yield_correlation", "temperature_yield_correlation"]] = correlation[
        ["rainfall_yield_correlation", "temperature_yield_correlation"]
    ].fillna(0.0).round(4)

    return observations, correlation


def _build_climate_impact_analysis(observations: pd.DataFrame) -> pd.DataFrame:
    climate = observations.copy()

    rainfall_mean = climate.groupby("region_id")["rainfall_mm"].transform("mean")
    rainfall_std = climate.groupby("region_id")["rainfall_mm"].transform("std").replace(0, 1).fillna(1)
    temp_mean = climate.groupby("region_id")["temperature_c"].transform("mean")
    temp_std = climate.groupby("region_id")["temperature_c"].transform("std").replace(0, 1).fillna(1)

    climate["rainfall_anomaly"] = ((climate["rainfall_mm"] - rainfall_mean) / rainfall_std).round(4)
    climate["temperature_anomaly"] = ((climate["temperature_c"] - temp_mean) / temp_std).round(4)
    climate["climate_stress_index"] = (
        climate["rainfall_anomaly"].abs() * 0.45 + climate["temperature_anomaly"].abs() * 0.55
    ).round(4)
    climate["estimated_productivity_impact_pct"] = (-climate["climate_stress_index"] * 8.5).round(3)

    percentile_rank = climate["climate_stress_index"].rank(pct=True, method="average")
    climate["climate_stress_level"] = "high"
    climate.loc[percentile_rank <= 0.33, "climate_stress_level"] = "low"
    climate.loc[(percentile_rank > 0.33) & (percentile_rank <= 0.66), "climate_stress_level"] = "moderate"

    return climate[
        [
            "date",
            "region_id",
            "crop",
            "yield_tph",
            "rainfall_mm",
            "temperature_c",
            "rainfall_anomaly",
            "temperature_anomaly",
            "climate_stress_index",
            "climate_stress_level",
            "estimated_productivity_impact_pct",
        ]
    ].sort_values(["region_id", "date"])


def export_powerbi_ready_data(
    source_path: Path | None = None,
    output_dir: Path = Path("dashboards/powerbi_exports/output"),
    climate_path: Path = Path("datasets/processed/climate_history.csv"),
    productivity_history_path: Path = Path("datasets/processed/productivity_history.csv"),
    dashboard_output_dir: Path = Path("dashboards/analytics/output"),
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    dashboard_output_dir.mkdir(parents=True, exist_ok=True)

    crop_df = _load_crop_data(source_path)
    climate_df = _load_climate_data(climate_path)
    productivity_history_df = _load_productivity_history(productivity_history_path)

    productivity_trends = _build_crop_productivity_trends(crop_df, productivity_history_df)
    rainfall_observations, rainfall_correlation = _build_rainfall_correlation(crop_df, climate_df)
    climate_impact = _build_climate_impact_analysis(rainfall_observations)
    kpis = pd.DataFrame([compute_kpis_from_frame(crop_df)])

    trends_path = output_dir / "crop_productivity_trends.csv"
    rainfall_obs_path = output_dir / "rainfall_correlation_observations.csv"
    rainfall_corr_path = output_dir / "rainfall_correlation_summary.csv"
    climate_impact_path = output_dir / "climate_impact_analysis.csv"
    kpi_path = output_dir / "kpis.csv"

    productivity_trends.to_csv(trends_path, index=False)
    rainfall_observations.to_csv(rainfall_obs_path, index=False)
    rainfall_correlation.to_csv(rainfall_corr_path, index=False)
    climate_impact.to_csv(climate_impact_path, index=False)
    kpis.to_csv(kpi_path, index=False)

    powerbi_parquet_path = output_dir / "agrix_powerbi_dataset.parquet"
    wide_dataset = productivity_trends.merge(
        climate_impact.loc[:, ["date", "region_id", "crop", "climate_stress_index", "climate_stress_level", "estimated_productivity_impact_pct"]],
        on=["date", "region_id", "crop"],
        how="left",
    )
    wide_dataset.to_parquet(powerbi_parquet_path, index=False)

    manifest_path = output_dir / "powerbi_manifest.json"
    manifest = {
        "tables": [
            {"name": "crop_productivity_trends", "path": str(trends_path)},
            {"name": "rainfall_correlation_observations", "path": str(rainfall_obs_path)},
            {"name": "rainfall_correlation_summary", "path": str(rainfall_corr_path)},
            {"name": "climate_impact_analysis", "path": str(climate_impact_path)},
            {"name": "kpis", "path": str(kpi_path)},
            {"name": "agrix_powerbi_dataset", "path": str(powerbi_parquet_path)},
        ],
        "relationships": [
            {"left": "crop_productivity_trends.region_id", "right": "climate_impact_analysis.region_id"},
            {"left": "crop_productivity_trends.date", "right": "climate_impact_analysis.date"},
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    productivity_dashboard_path = dashboard_output_dir / "crop_productivity_trends_dashboard.html"
    rainfall_dashboard_path = dashboard_output_dir / "rainfall_correlation_dashboard.html"
    climate_dashboard_path = dashboard_output_dir / "climate_impact_dashboard.html"

    build_productivity_trends_dashboard(productivity_trends, productivity_dashboard_path)
    build_rainfall_correlation_dashboard(rainfall_observations, rainfall_correlation, rainfall_dashboard_path)
    build_climate_impact_dashboard(climate_impact, climate_dashboard_path)

    return {
        "crop_productivity_trends": trends_path,
        "rainfall_correlation_observations": rainfall_obs_path,
        "rainfall_correlation_summary": rainfall_corr_path,
        "climate_impact_analysis": climate_impact_path,
        "kpis": kpi_path,
        "powerbi_dataset": powerbi_parquet_path,
        "powerbi_manifest": manifest_path,
        "dashboard_productivity": productivity_dashboard_path,
        "dashboard_rainfall": rainfall_dashboard_path,
        "dashboard_climate_impact": climate_dashboard_path,
    }


if __name__ == "__main__":
    exported = export_powerbi_ready_data()
    print({key: str(value) for key, value in exported.items()})
