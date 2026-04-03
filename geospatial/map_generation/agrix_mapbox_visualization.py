from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

try:
    import geopandas as gpd
except Exception:  # pragma: no cover
    gpd = None


@dataclass(slots=True)
class VisualizationConfig:
    productivity_csv: Path = Path("datasets/processed/region_productivity.csv")
    climate_csv: Path = Path("datasets/processed/climate_history.csv")
    output_dir: Path = Path("geospatial/map_generation/output")
    map_center_lon: float = 78.5
    map_center_lat: float = 22.5
    map_zoom: float = 4.0
    productivity_buffer_meters: float = 30000.0


class AgriXMapboxVisualizer:
    def __init__(self, config: VisualizationConfig | None = None):
        self.config = config or VisualizationConfig()

    @staticmethod
    def _require_geopandas() -> None:
        if gpd is None:
            raise ImportError("GeoPandas is required for geospatial visualization. Install geopandas to continue.")

    def load_base_geodata(self) -> "gpd.GeoDataFrame":
        self._require_geopandas()
        prod = pd.read_csv(self.config.productivity_csv)
        required_cols = {"region_id", "latitude", "longitude", "yield_tph", "avg_ndvi"}
        missing = required_cols - set(prod.columns)
        if missing:
            raise ValueError(f"Missing productivity columns: {sorted(missing)}")

        climate = pd.read_csv(self.config.climate_csv)
        if "region_id" in climate.columns and "rainfall_mm" in climate.columns:
            rainfall = climate.groupby("region_id", as_index=False)["rainfall_mm"].mean().rename(
                columns={"rainfall_mm": "avg_rainfall_mm"}
            )
            merged = prod.merge(rainfall, on="region_id", how="left")
        else:
            merged = prod.copy()
            merged["avg_rainfall_mm"] = 0.0

        merged["avg_rainfall_mm"] = pd.to_numeric(merged["avg_rainfall_mm"], errors="coerce").fillna(
            merged["avg_rainfall_mm"].mean()
        )
        merged["yield_tph"] = pd.to_numeric(merged["yield_tph"], errors="coerce")
        merged["avg_ndvi"] = pd.to_numeric(merged["avg_ndvi"], errors="coerce")
        merged = merged.dropna(subset=["yield_tph", "avg_ndvi", "latitude", "longitude"]).reset_index(drop=True)

        base_gdf = gpd.GeoDataFrame(
            merged,
            geometry=gpd.points_from_xy(merged["longitude"], merged["latitude"]),
            crs="EPSG:4326",
        )
        return base_gdf

    def build_crop_productivity_map(self, base_gdf: "gpd.GeoDataFrame") -> "gpd.GeoDataFrame":
        self._require_geopandas()
        projected = base_gdf.to_crs("EPSG:3857")
        projected["geometry"] = projected.geometry.buffer(self.config.productivity_buffer_meters)
        productivity_map = projected.to_crs("EPSG:4326")
        productivity_map["productivity_score"] = productivity_map["yield_tph"]
        return productivity_map[["region_id", "yield_tph", "avg_ndvi", "avg_rainfall_mm", "productivity_score", "geometry"]]

    def build_rainfall_heatmap(self, base_gdf: "gpd.GeoDataFrame") -> "gpd.GeoDataFrame":
        self._require_geopandas()
        rainfall = base_gdf.copy()
        rainfall["rainfall_intensity"] = rainfall["avg_rainfall_mm"]
        return rainfall[["region_id", "avg_rainfall_mm", "rainfall_intensity", "geometry"]]

    def build_ndvi_vegetation_map(self, base_gdf: "gpd.GeoDataFrame") -> "gpd.GeoDataFrame":
        self._require_geopandas()
        ndvi = base_gdf.copy()
        ndvi["vegetation_score"] = ndvi["avg_ndvi"]
        return ndvi[["region_id", "avg_ndvi", "vegetation_score", "yield_tph", "geometry"]]

    def export_geojson_layers(self, output_dir: Path | None = None) -> dict[str, Path]:
        self._require_geopandas()
        out_dir = output_dir or self.config.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        base_gdf = self.load_base_geodata()
        productivity = self.build_crop_productivity_map(base_gdf)
        rainfall = self.build_rainfall_heatmap(base_gdf)
        ndvi = self.build_ndvi_vegetation_map(base_gdf)

        productivity_path = out_dir / "crop_productivity.geojson"
        rainfall_path = out_dir / "rainfall_heatmap.geojson"
        ndvi_path = out_dir / "ndvi_vegetation.geojson"

        productivity.to_file(productivity_path, driver="GeoJSON")
        rainfall.to_file(rainfall_path, driver="GeoJSON")
        ndvi.to_file(ndvi_path, driver="GeoJSON")

        return {
            "crop_productivity": productivity_path,
            "rainfall_heatmap": rainfall_path,
            "ndvi_vegetation": ndvi_path,
        }

    def build_mapbox_style(self, geojson_paths: dict[str, Path], output_dir: Path | None = None) -> Path:
        out_dir = output_dir or self.config.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        style_path = out_dir / "mapbox_style.json"

        style = {
            "version": 8,
            "name": "AgriX Geospatial Visualization",
            "sources": {
                "crop_productivity": {"type": "geojson", "data": str(geojson_paths["crop_productivity"])},
                "rainfall_heatmap": {"type": "geojson", "data": str(geojson_paths["rainfall_heatmap"])},
                "ndvi_vegetation": {"type": "geojson", "data": str(geojson_paths["ndvi_vegetation"])},
            },
            "layers": [
                {"id": "background", "type": "background", "paint": {"background-color": "#edf4e8"}},
                {
                    "id": "crop-productivity-fill",
                    "type": "fill",
                    "source": "crop_productivity",
                    "paint": {
                        "fill-color": [
                            "interpolate",
                            ["linear"],
                            ["get", "yield_tph"],
                            2.5,
                            "#fde68a",
                            3.5,
                            "#86efac",
                            5.0,
                            "#166534",
                        ],
                        "fill-opacity": 0.45,
                    },
                },
                {
                    "id": "crop-productivity-outline",
                    "type": "line",
                    "source": "crop_productivity",
                    "paint": {"line-color": "#14532d", "line-width": 1.0},
                },
                {
                    "id": "rainfall-heatmap",
                    "type": "heatmap",
                    "source": "rainfall_heatmap",
                    "paint": {
                        "heatmap-weight": [
                            "interpolate",
                            ["linear"],
                            ["get", "avg_rainfall_mm"],
                            0,
                            0,
                            220,
                            1,
                        ],
                        "heatmap-intensity": 0.9,
                        "heatmap-radius": 28,
                        "heatmap-color": [
                            "interpolate",
                            ["linear"],
                            ["heatmap-density"],
                            0.0,
                            "rgba(59,130,246,0)",
                            0.3,
                            "#93c5fd",
                            0.6,
                            "#3b82f6",
                            1.0,
                            "#1e3a8a",
                        ],
                    },
                },
                {
                    "id": "ndvi-vegetation-points",
                    "type": "circle",
                    "source": "ndvi_vegetation",
                    "paint": {
                        "circle-radius": [
                            "interpolate",
                            ["linear"],
                            ["get", "avg_ndvi"],
                            0.3,
                            5,
                            0.8,
                            14,
                        ],
                        "circle-color": [
                            "interpolate",
                            ["linear"],
                            ["get", "avg_ndvi"],
                            0.2,
                            "#f59e0b",
                            0.5,
                            "#84cc16",
                            0.8,
                            "#14532d",
                        ],
                        "circle-stroke-color": "#ffffff",
                        "circle-stroke-width": 1.0,
                    },
                },
            ],
        }
        style_path.write_text(json.dumps(style, indent=2), encoding="utf-8")
        return style_path

    def build_mapbox_html(self, geojson_paths: dict[str, Path], mapbox_token: str, output_dir: Path | None = None) -> Path:
        out_dir = output_dir or self.config.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        html_path = out_dir / "mapbox_visualization.html"

        html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AgriX Geospatial Maps</title>
    <script src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css" rel="stylesheet" />
    <style>
      body {{ margin: 0; font-family: Arial, sans-serif; }}
      #map {{ position: absolute; top: 0; bottom: 0; width: 100%; }}
      .panel {{
        position: absolute; top: 12px; left: 12px; z-index: 2; background: rgba(255,255,255,0.92);
        padding: 10px 12px; border-radius: 8px; box-shadow: 0 8px 20px rgba(0,0,0,0.15);
      }}
      .panel label {{ display: block; margin: 6px 0; }}
    </style>
  </head>
  <body>
    <div id="map"></div>
    <div class="panel">
      <strong>AgriX Layers</strong>
      <label><input id="toggle-productivity" type="checkbox" checked /> Crop Productivity</label>
      <label><input id="toggle-rainfall" type="checkbox" checked /> Rainfall Heatmap</label>
      <label><input id="toggle-ndvi" type="checkbox" checked /> NDVI Vegetation</label>
    </div>
    <script>
      mapboxgl.accessToken = "{mapbox_token}";
      const map = new mapboxgl.Map({{
        container: "map",
        style: "mapbox://styles/mapbox/satellite-streets-v12",
        center: [{self.config.map_center_lon}, {self.config.map_center_lat}],
        zoom: {self.config.map_zoom}
      }});

      map.on("load", () => {{
        map.addSource("crop_productivity", {{ type: "geojson", data: "{geojson_paths["crop_productivity"]}" }});
        map.addSource("rainfall_heatmap", {{ type: "geojson", data: "{geojson_paths["rainfall_heatmap"]}" }});
        map.addSource("ndvi_vegetation", {{ type: "geojson", data: "{geojson_paths["ndvi_vegetation"]}" }});

        map.addLayer({{
          id: "crop-productivity-fill",
          type: "fill",
          source: "crop_productivity",
          paint: {{
            "fill-color": ["interpolate", ["linear"], ["get", "yield_tph"], 2.5, "#fde68a", 3.5, "#86efac", 5.0, "#166534"],
            "fill-opacity": 0.45
          }}
        }});
        map.addLayer({{
          id: "crop-productivity-outline",
          type: "line",
          source: "crop_productivity",
          paint: {{ "line-color": "#14532d", "line-width": 1.0 }}
        }});
        map.addLayer({{
          id: "rainfall-heatmap",
          type: "heatmap",
          source: "rainfall_heatmap",
          paint: {{
            "heatmap-weight": ["interpolate", ["linear"], ["get", "avg_rainfall_mm"], 0, 0, 220, 1],
            "heatmap-intensity": 0.9,
            "heatmap-radius": 28,
            "heatmap-color": ["interpolate", ["linear"], ["heatmap-density"], 0.0, "rgba(59,130,246,0)", 0.3, "#93c5fd", 0.6, "#3b82f6", 1.0, "#1e3a8a"]
          }}
        }});
        map.addLayer({{
          id: "ndvi-vegetation-points",
          type: "circle",
          source: "ndvi_vegetation",
          paint: {{
            "circle-radius": ["interpolate", ["linear"], ["get", "avg_ndvi"], 0.3, 5, 0.8, 14],
            "circle-color": ["interpolate", ["linear"], ["get", "avg_ndvi"], 0.2, "#f59e0b", 0.5, "#84cc16", 0.8, "#14532d"],
            "circle-stroke-color": "#ffffff",
            "circle-stroke-width": 1.0
          }}
        }});
      }});

      const setVisibility = (layerIds, visible) => {{
        layerIds.forEach((id) => {{
          if (map.getLayer(id)) map.setLayoutProperty(id, "visibility", visible ? "visible" : "none");
        }});
      }};

      document.getElementById("toggle-productivity").addEventListener("change", (e) => {{
        setVisibility(["crop-productivity-fill", "crop-productivity-outline"], e.target.checked);
      }});
      document.getElementById("toggle-rainfall").addEventListener("change", (e) => {{
        setVisibility(["rainfall-heatmap"], e.target.checked);
      }});
      document.getElementById("toggle-ndvi").addEventListener("change", (e) => {{
        setVisibility(["ndvi-vegetation-points"], e.target.checked);
      }});
    </script>
  </body>
</html>
"""
        html_path.write_text(html, encoding="utf-8")
        return html_path

    def build_visualization_bundle(self, mapbox_token: str, output_dir: Path | None = None) -> dict[str, Path]:
        out_dir = output_dir or self.config.output_dir
        geojson_paths = self.export_geojson_layers(out_dir)
        style_path = self.build_mapbox_style(geojson_paths=geojson_paths, output_dir=out_dir)
        html_path = self.build_mapbox_html(geojson_paths=geojson_paths, mapbox_token=mapbox_token, output_dir=out_dir)
        return {
            **geojson_paths,
            "mapbox_style": style_path,
            "mapbox_html": html_path,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AgriX GeoPandas + Mapbox visualization layers and viewer.")
    parser.add_argument("--mapbox-token", required=True, help="Mapbox public access token.")
    parser.add_argument("--productivity-csv", default="datasets/processed/region_productivity.csv")
    parser.add_argument("--climate-csv", default="datasets/processed/climate_history.csv")
    parser.add_argument("--output-dir", default="geospatial/map_generation/output")
    args = parser.parse_args()

    visualizer = AgriXMapboxVisualizer(
        VisualizationConfig(
            productivity_csv=Path(args.productivity_csv),
            climate_csv=Path(args.climate_csv),
            output_dir=Path(args.output_dir),
        )
    )
    outputs = visualizer.build_visualization_bundle(mapbox_token=args.mapbox_token)
    print({key: str(value) for key, value in outputs.items()})


if __name__ == "__main__":
    main()
