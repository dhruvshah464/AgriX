import { useState } from 'react';
import { MapPin, Sprout, Droplets, Activity, LayoutGrid, List, Search, Filter } from 'lucide-react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import Input from '../components/ui/Input';
import { fieldsData } from '../data/mockData';

const healthConfig = {
  excellent: { variant: 'green', label: 'Excellent' },
  good:      { variant: 'teal', label: 'Good' },
  warning:   { variant: 'amber', label: 'Warning' },
  critical:  { variant: 'red', label: 'Critical' },
};

export default function FieldsPage() {
  const [view, setView] = useState('grid');
  const [search, setSearch] = useState('');
  const [healthFilter, setHealthFilter] = useState('all');

  const filtered = fieldsData.filter((f) => {
    const matchesSearch = f.name.toLowerCase().includes(search.toLowerCase()) ||
      f.crop.toLowerCase().includes(search.toLowerCase());
    const matchesHealth = healthFilter === 'all' || f.health === healthFilter;
    return matchesSearch && matchesHealth;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-slate-800">My Fields</h1>
          <p className="text-sm text-slate-500 mt-0.5">{fieldsData.length} fields under management</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setView('grid')}
            className={`btn-icon ${view === 'grid' ? 'bg-green-50 text-green-600' : ''}`}
          >
            <LayoutGrid size={18} />
          </button>
          <button
            onClick={() => setView('list')}
            className={`btn-icon ${view === 'list' ? 'bg-green-50 text-green-600' : ''}`}
          >
            <List size={18} />
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-3 flex-wrap">
        <div className="flex-1 min-w-[200px] max-w-sm">
          <Input
            icon={Search}
            placeholder="Search fields or crops..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            id="field-search"
          />
        </div>
        <div className="flex gap-1.5">
          {['all', 'excellent', 'good', 'warning', 'critical'].map((h) => (
            <button
              key={h}
              onClick={() => setHealthFilter(h)}
              className={`px-3 py-1.5 text-xs font-medium rounded-full transition-all ${
                healthFilter === h
                  ? 'bg-green-600 text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {h === 'all' ? 'All' : h.charAt(0).toUpperCase() + h.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Grid View */}
      {view === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map((field) => {
            const health = healthConfig[field.health];
            return (
              <Card key={field.id} className="hover:-translate-y-0.5" padding="p-0">
                {/* Gradient header */}
                <div className="h-3 bg-gradient-to-r from-green-400 to-emerald-500 rounded-t-xl" />
                <div className="p-5">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-sm font-semibold text-slate-800">{field.name}</h3>
                      <p className="text-xs text-slate-500 flex items-center gap-1 mt-1">
                        <MapPin size={12} /> {field.area} {field.unit}
                      </p>
                    </div>
                    <Badge variant={health.variant} dot>{health.label}</Badge>
                  </div>

                  <div className="mt-4 grid grid-cols-2 gap-3">
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-lg bg-green-50 flex items-center justify-center">
                        <Sprout size={14} className="text-green-600" />
                      </div>
                      <div>
                        <p className="text-[10px] text-slate-400">Crop</p>
                        <p className="text-xs font-medium text-slate-700">{field.crop}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-lg bg-blue-50 flex items-center justify-center">
                        <Droplets size={14} className="text-blue-600" />
                      </div>
                      <div>
                        <p className="text-[10px] text-slate-400">Moisture</p>
                        <p className="text-xs font-medium text-slate-700">{field.soilMoisture}%</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-lg bg-amber-50 flex items-center justify-center">
                        <Activity size={14} className="text-amber-600" />
                      </div>
                      <div>
                        <p className="text-[10px] text-slate-400">NDVI</p>
                        <p className="text-xs font-medium text-slate-700">{field.ndvi}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-lg bg-teal-50 flex items-center justify-center">
                        <Sprout size={14} className="text-teal-600" />
                      </div>
                      <div>
                        <p className="text-[10px] text-slate-400">Stage</p>
                        <p className="text-xs font-medium text-slate-700">{field.growthStage}</p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                    <span className="text-[10px] text-slate-400">Irrigated {field.lastIrrigated}</span>
                    <span className="text-xs font-semibold text-green-600">{field.daysToHarvest}d to harvest</span>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      ) : (
        /* List View */
        <Card padding="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-100">
                  <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Field</th>
                  <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Crop</th>
                  <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Area</th>
                  <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Health</th>
                  <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Moisture</th>
                  <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Harvest</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {filtered.map((field) => {
                  const health = healthConfig[field.health];
                  return (
                    <tr key={field.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="px-5 py-3 font-medium text-slate-800">{field.name}</td>
                      <td className="px-5 py-3 text-slate-600">{field.crop}</td>
                      <td className="px-5 py-3 text-slate-600">{field.area} {field.unit}</td>
                      <td className="px-5 py-3"><Badge variant={health.variant} dot>{health.label}</Badge></td>
                      <td className="px-5 py-3 text-slate-600">{field.soilMoisture}%</td>
                      <td className="px-5 py-3 font-medium text-green-600">{field.daysToHarvest}d</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </div>
  );
}
