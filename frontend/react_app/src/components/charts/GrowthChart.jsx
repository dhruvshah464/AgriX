import { useState, memo } from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import Card from '../ui/Card';

const metrics = [
  { key: 'height', label: 'Height (cm)', color: '#16a34a', gradient: ['#16a34a', '#16a34a00'] },
  { key: 'biomass', label: 'Biomass (t/ha)', color: '#3b82f6', gradient: ['#3b82f6', '#3b82f600'] },
  { key: 'lai', label: 'LAI Index', color: '#f59e0b', gradient: ['#f59e0b', '#f59e0b00'] },
];

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="custom-tooltip">
      <p className="text-xs font-semibold text-slate-700 mb-1">{label}</p>
      {payload.map((entry) => (
        <p key={entry.name} className="text-xs text-slate-600 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full" style={{ background: entry.color }} />
          {entry.name}: <span className="font-semibold">{entry.value}</span>
        </p>
      ))}
    </div>
  );
}

const GrowthChart = memo(function GrowthChart({ data }) {
  const [activeMetric, setActiveMetric] = useState(0);
  const metric = metrics[activeMetric];

  return (
    <Card padding="p-0" className="overflow-hidden">
      <div className="px-5 pt-5 pb-3 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-slate-800">Crop Growth Monitoring</h3>
          <p className="text-xs text-slate-400 mt-0.5">Weekly progression metrics</p>
        </div>
        <div className="flex gap-1 bg-slate-100 rounded-lg p-0.5">
          {metrics.map((m, i) => (
            <button
              key={m.key}
              onClick={() => setActiveMetric(i)}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all duration-200 ${
                i === activeMetric
                  ? 'bg-white text-slate-800 shadow-sm'
                  : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              {m.label.split(' ')[0]}
            </button>
          ))}
        </div>
      </div>

      <div className="px-3 pb-4 h-64 chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <defs>
              <linearGradient id={`grad-${metric.key}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={metric.gradient[0]} stopOpacity={0.3} />
                <stop offset="100%" stopColor={metric.gradient[1]} stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis
              dataKey="week"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: '#94a3b8' }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: '#94a3b8' }}
              width={40}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey={metric.key}
              stroke={metric.color}
              fill={`url(#grad-${metric.key})`}
              strokeWidth={2.5}
              dot={{ r: 3, fill: 'white', stroke: metric.color, strokeWidth: 2 }}
              activeDot={{ r: 5, fill: metric.color, stroke: 'white', strokeWidth: 2 }}
              animationDuration={500}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
});

export default GrowthChart;
