import { memo } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import Card from '../ui/Card';

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="custom-tooltip">
      <p className="text-xs font-semibold text-slate-700 mb-1">{label}</p>
      {payload.map((entry) => (
        <p key={entry.name} className="text-xs text-slate-600 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full" style={{ background: entry.color }} />
          {entry.name}: <span className="font-semibold">{entry.value}{entry.name.includes('mm') ? 'mm' : '°C'}</span>
        </p>
      ))}
    </div>
  );
}

const ClimateChart = memo(function ClimateChart({ data }) {
  return (
    <Card padding="p-0" className="overflow-hidden">
      <div className="px-5 pt-5 pb-3">
        <h3 className="text-sm font-semibold text-slate-800">Climate Forecast</h3>
        <p className="text-xs text-slate-400 mt-0.5">Temperature and rainfall projections</p>
      </div>

      <div className="px-3 pb-4 h-64 chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#94a3b8' }} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#94a3b8' }} width={35} />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              iconType="circle"
              iconSize={8}
              wrapperStyle={{ fontSize: '11px', color: '#64748b', paddingTop: '8px' }}
            />
            <Bar dataKey="rainfall_mm" name="Rainfall (mm)" fill="#3b82f6" radius={[4, 4, 0, 0]} barSize={18} />
            <Bar dataKey="temperature_c" name="Temp (°C)" fill="#f59e0b" radius={[4, 4, 0, 0]} barSize={18} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
});

export default ClimateChart;
