import { Cloud, Droplets, Wind, Sun, Eye } from 'lucide-react';
import Card from '../ui/Card';

export default function WeatherWidget({ weather }) {
  return (
    <Card className="overflow-hidden" padding="p-0">
      {/* Current weather */}
      <div className="p-5 bg-gradient-to-br from-blue-50 to-sky-50">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">Current Weather</p>
            <div className="flex items-end gap-2 mt-2">
              <span className="text-4xl font-bold text-slate-800">{weather.current.temp}°</span>
              <span className="text-sm text-slate-500 pb-1">Feels {weather.current.feelsLike}°</span>
            </div>
            <p className="text-sm text-slate-600 mt-1 flex items-center gap-1.5">
              <Cloud size={14} className="text-blue-500" />
              {weather.current.condition}
            </p>
          </div>
          <div className="text-5xl">⛅</div>
        </div>

        {/* Quick stats */}
        <div className="grid grid-cols-3 gap-3 mt-4">
          <div className="flex items-center gap-2 text-xs text-slate-600">
            <Droplets size={13} className="text-blue-500" />
            <span>{weather.current.humidity}%</span>
          </div>
          <div className="flex items-center gap-2 text-xs text-slate-600">
            <Wind size={13} className="text-slate-400" />
            <span>{weather.current.windSpeed} km/h</span>
          </div>
          <div className="flex items-center gap-2 text-xs text-slate-600">
            <Sun size={13} className="text-amber-500" />
            <span>UV {weather.current.uvIndex}</span>
          </div>
        </div>
      </div>

      {/* Forecast row */}
      <div className="grid grid-cols-5 divide-x divide-slate-100 border-t border-slate-100">
        {weather.forecast.map((day) => (
          <div key={day.day} className="py-3 px-2 text-center hover:bg-slate-50 transition-colors">
            <p className="text-[10px] font-semibold text-slate-500 uppercase">{day.day}</p>
            <p className="text-lg my-1">{day.icon}</p>
            <p className="text-xs font-semibold text-slate-700">{day.high}°</p>
            <p className="text-[10px] text-slate-400">{day.low}°</p>
            {day.rain > 0 && (
              <p className="text-[10px] text-blue-500 mt-0.5 flex items-center justify-center gap-0.5">
                <Droplets size={8} />{day.rain}%
              </p>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
}
