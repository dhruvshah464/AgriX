import { useEffect, useState } from 'react';
import { CloudSun } from 'lucide-react';
import ClimateChart from '../components/charts/ClimateChart';
import WeatherWidget from '../components/widgets/WeatherWidget';
import { fetchClimateForecast } from '../services/apiClient';
import { weatherData } from '../data/mockData';
import { SkeletonChart } from '../components/ui/Skeleton';

export default function ForecastPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setLoading(true);
    fetchClimateForecast({ region_id: 'delhi-ncr', horizon_days: 7 })
      .then((response) => {
        setData(
          response.points.map((point) => ({
            date: point.date.slice(5),
            rainfall_mm: point.rainfall_mm,
            temperature_c: point.temperature_c,
          }))
        );
      })
      .catch(() => {
        setError('Backend API unavailable. Showing demo weather data.');
        // Fallback demo data
        setData([
          { date: '04-03', rainfall_mm: 12, temperature_c: 29 },
          { date: '04-04', rainfall_mm: 5, temperature_c: 32 },
          { date: '04-05', rainfall_mm: 45, temperature_c: 28 },
          { date: '04-06', rainfall_mm: 38, temperature_c: 26 },
          { date: '04-07', rainfall_mm: 15, temperature_c: 30 },
          { date: '04-08', rainfall_mm: 8, temperature_c: 31 },
          { date: '04-09', rainfall_mm: 2, temperature_c: 33 },
        ]);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-sky-600 flex items-center justify-center">
          <CloudSun size={20} className="text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-slate-800">Climate Forecast</h1>
          <p className="text-sm text-slate-500">7-day agricultural weather intelligence</p>
        </div>
      </div>

      {error && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg px-4 py-3 text-sm text-amber-700">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          {loading ? <SkeletonChart /> : <ClimateChart data={data} />}
        </div>
        <div>
          <WeatherWidget weather={weatherData} />
        </div>
      </div>
    </div>
  );
}
