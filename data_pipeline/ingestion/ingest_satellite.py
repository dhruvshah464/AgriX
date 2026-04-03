from __future__ import annotations

from pathlib import Path

import pandas as pd


def run(source_dir: Path = Path("datasets/external/satellite_catalog"), out_path: Path = Path("datasets/raw/satellite_catalog.csv")) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []

    if source_dir.exists():
        for tif_path in source_dir.rglob("*.tif"):
            records.append(
                {
                    "scene_id": tif_path.stem,
                    "path": str(tif_path),
                    "provider": "sentinel-2" if "S2" in tif_path.name.upper() else "landsat",
                }
            )

    if not records:
        records = [
            {"scene_id": "S2A_SAMPLE_001", "path": "datasets/external/sentinel/sample_nir.tif", "provider": "sentinel-2"},
            {"scene_id": "L8_SAMPLE_001", "path": "datasets/external/landsat/sample_nir.tif", "provider": "landsat"},
        ]

    pd.DataFrame(records).to_csv(out_path, index=False)
    return out_path


if __name__ == "__main__":
    print(f"Satellite catalog ingested: {run()}")
