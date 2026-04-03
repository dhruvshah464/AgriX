import { MapPin, Sprout, Clock, Droplets } from 'lucide-react';
import Badge from '../ui/Badge';

const healthColors = {
  excellent: 'green',
  good: 'teal',
  warning: 'amber',
  critical: 'red',
};

const fieldGradients = [
  'from-green-400 via-emerald-500 to-teal-600',
  'from-emerald-400 via-green-500 to-green-700',
  'from-teal-400 via-emerald-500 to-green-600',
  'from-green-500 via-emerald-600 to-teal-700',
];

export default function FieldHero({ field, index = 0 }) {
  const gradient = fieldGradients[index % fieldGradients.length];

  return (
    <div className="relative overflow-hidden rounded-xl bg-white border border-slate-100 shadow-card hover:shadow-card-hover transition-all duration-300 group">
      {/* Gradient Hero */}
      <div className={`h-36 bg-gradient-to-br ${gradient} relative overflow-hidden`}>
        {/* Pattern overlay */}
        <div className="absolute inset-0 opacity-10" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }} />

        {/* Field info overlay */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/50 to-transparent p-4">
          <h3 className="text-white font-bold text-lg">{field.name}</h3>
          <div className="flex items-center gap-3 mt-1">
            <span className="text-white/80 text-xs flex items-center gap-1">
              <MapPin size={12} /> {field.area} {field.unit}
            </span>
            <span className="text-white/80 text-xs flex items-center gap-1">
              <Sprout size={12} /> {field.crop} · {field.variety}
            </span>
          </div>
        </div>

        {/* Health badge */}
        <div className="absolute top-3 right-3">
          <Badge variant={healthColors[field.health]} dot>
            {field.health}
          </Badge>
        </div>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-3 divide-x divide-slate-100 p-0">
        <div className="px-4 py-3 text-center">
          <p className="text-xs text-slate-500">Growth Stage</p>
          <p className="text-sm font-semibold text-slate-800 mt-0.5">{field.growthStage}</p>
        </div>
        <div className="px-4 py-3 text-center">
          <p className="text-xs text-slate-500 flex items-center justify-center gap-1"><Clock size={11} /> Harvest</p>
          <p className="text-sm font-semibold text-slate-800 mt-0.5">{field.daysToHarvest}d</p>
        </div>
        <div className="px-4 py-3 text-center">
          <p className="text-xs text-slate-500 flex items-center justify-center gap-1"><Droplets size={11} /> Moisture</p>
          <p className="text-sm font-semibold text-slate-800 mt-0.5">{field.soilMoisture}%</p>
        </div>
      </div>
    </div>
  );
}
