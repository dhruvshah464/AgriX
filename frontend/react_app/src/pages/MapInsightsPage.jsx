import { useEffect, useState, useRef } from 'react';
import { Map as MapIcon } from 'lucide-react';
import mapboxgl from 'mapbox-gl';
import Card from '../components/ui/Card';
import { fetchProductivityMap } from '../services/apiClient';

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;

const mapModes = [
  { id: 'productivity', label: 'Crop Productivity', dataKey: 'yield_tph', colors: ['#fde68a', '#16a34a'], range: [2.5, 5] },
  { id: 'rainfall', label: 'Rainfall Heatmap', dataKey: 'avg_rainfall_mm', colors: ['#93c5fd', '#1e3a8a'], range: [20, 200] },
  { id: 'ndvi', label: 'NDVI Vegetation', dataKey: 'avg_ndvi', colors: ['#f59e0b', '#14532d'], range: [0.2, 0.8] },
];

export default function MapInsightsPage() {
  const [geojson, setGeojson] = useState({ type: 'FeatureCollection', features: [] });
  const [mapMode, setMapMode] = useState('productivity');
  const [error, setError] = useState('');
  const mapRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    fetchProductivityMap({ region_id: 'delhi-ncr' })
      .then((response) => setGeojson(response.geojson))
      .catch(() => setError('Could not load geospatial productivity layer. Using default view.'));
  }, []);

  useEffect(() => {
    if (!containerRef.current || !MAPBOX_TOKEN) return;

    mapboxgl.accessToken = MAPBOX_TOKEN;
    const map = new mapboxgl.Map({
      container: containerRef.current,
      style: 'mapbox://styles/mapbox/satellite-streets-v12',
      center: [77.21, 28.63],
      zoom: 5,
    });

    map.on('load', () => {
      if (geojson.features.length > 0) {
        map.addSource('productivity', { type: 'geojson', data: geojson });
        const mode = mapModes.find(m => m.id === mapMode);
        map.addLayer({
          id: 'productivity-points',
          type: 'circle',
          source: 'productivity',
          paint: {
            'circle-color': ['interpolate', ['linear'], ['get', mode.dataKey], mode.range[0], mode.colors[0], mode.range[1], mode.colors[1]],
            'circle-radius': ['interpolate', ['linear'], ['get', mode.dataKey], mode.range[0], 6, mode.range[1], 16],
            'circle-stroke-color': '#ffffff',
            'circle-stroke-width': 1.5,
            'circle-opacity': 0.9,
          },
        });
      }
    });

    map.addControl(new mapboxgl.NavigationControl(), 'top-right');
    mapRef.current = map;

    return () => map.remove();
  }, [geojson, mapMode]);

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
          <MapIcon size={20} className="text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-slate-800">Geospatial Intelligence</h1>
          <p className="text-sm text-slate-500">Satellite-powered field analysis & mapping</p>
        </div>
      </div>

      {/* Map mode tabs */}
      <div className="flex gap-2 flex-wrap">
        {mapModes.map((mode) => (
          <button
            key={mode.id}
            onClick={() => setMapMode(mode.id)}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-all ${
              mapMode === mode.id
                ? 'bg-green-600 text-white shadow-sm'
                : 'bg-white text-slate-600 border border-slate-200 hover:border-slate-300'
            }`}
          >
            {mode.label}
          </button>
        ))}
      </div>

      {error && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg px-4 py-3 text-sm text-amber-700">
          {error}
        </div>
      )}

      {MAPBOX_TOKEN ? (
        <Card padding="p-0" className="overflow-hidden">
          <div ref={containerRef} className="h-[520px] w-full" />
        </Card>
      ) : (
        <Card className="text-center py-16">
          <MapIcon size={40} className="text-slate-300 mx-auto mb-4" />
          <h3 className="text-base font-semibold text-slate-700 mb-1">Map Requires Token</h3>
          <p className="text-sm text-slate-500">Set <code className="text-xs bg-slate-100 px-1 py-0.5 rounded">VITE_MAPBOX_TOKEN</code> to enable geospatial view.</p>
        </Card>
      )}
    </div>
  );
}
