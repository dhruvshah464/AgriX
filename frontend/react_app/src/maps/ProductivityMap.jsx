import mapboxgl from "mapbox-gl";
import { useEffect, useRef } from "react";

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;

function getMapPaintByMode(mapMode) {
  if (mapMode === "rainfall") {
    return {
      "circle-color": ["interpolate", ["linear"], ["get", "avg_rainfall_mm"], 20, "#93c5fd", 90, "#3b82f6", 180, "#1e3a8a"],
      "circle-radius": ["interpolate", ["linear"], ["get", "avg_rainfall_mm"], 20, 6, 200, 18],
      "circle-stroke-color": "#ffffff",
      "circle-stroke-width": 1.2,
      "circle-opacity": 0.9,
    };
  }

  if (mapMode === "ndvi") {
    return {
      "circle-color": ["interpolate", ["linear"], ["get", "avg_ndvi"], 0.2, "#f59e0b", 0.5, "#84cc16", 0.8, "#14532d"],
      "circle-radius": ["interpolate", ["linear"], ["get", "avg_ndvi"], 0.2, 5, 0.8, 16],
      "circle-stroke-color": "#ffffff",
      "circle-stroke-width": 1.2,
      "circle-opacity": 0.9,
    };
  }

  return {
    "circle-color": ["interpolate", ["linear"], ["get", "yield_tph"], 2.5, "#FCD34D", 5, "#166534"],
    "circle-radius": ["interpolate", ["linear"], ["get", "yield_tph"], 2.5, 6, 5.0, 16],
    "circle-stroke-color": "#ffffff",
    "circle-stroke-width": 1.5,
    "circle-opacity": 0.9,
  };
}

export default function ProductivityMap({ featureCollection, mapMode = "productivity" }) {
  const mapRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current || !MAPBOX_TOKEN) {
      return undefined;
    }

    mapboxgl.accessToken = MAPBOX_TOKEN;
    mapRef.current = new mapboxgl.Map({
      container: containerRef.current,
      style: "mapbox://styles/mapbox/satellite-streets-v12",
      center: [77.21, 28.63],
      zoom: 5,
    });

    mapRef.current.on("load", () => {
      mapRef.current.addSource("productivity", {
        type: "geojson",
        data: featureCollection,
      });
      mapRef.current.addLayer({
        id: "productivity-points",
        type: "circle",
        source: "productivity",
        paint: getMapPaintByMode(mapMode),
      });
    });

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
      }
    };
  }, [featureCollection, mapMode]);

  if (!MAPBOX_TOKEN) {
    return (
      <div className="rounded-2xl border border-amber-300 bg-amber-50 p-4 text-amber-800">
        Set <code>VITE_MAPBOX_TOKEN</code> in frontend env to render geospatial map.
      </div>
    );
  }

  return <div ref={containerRef} className="h-[480px] w-full rounded-2xl border border-white/70 shadow-panel" />;
}
