from __future__ import annotations

from pathlib import Path


def list_scenes(root: Path = Path("datasets/external/satellite_catalog")) -> list[dict]:
    scenes = []
    if root.exists():
        for tif in root.rglob("*.tif"):
            scenes.append(
                {
                    "scene_id": tif.stem,
                    "path": str(tif),
                    "provider": "sentinel-2" if "S2" in tif.name.upper() else "landsat",
                }
            )
    return scenes
