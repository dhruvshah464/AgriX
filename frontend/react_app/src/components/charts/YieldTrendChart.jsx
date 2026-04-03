import { memo } from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
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
          Yield: <span className="font-semibold">{entry.value} t/ha</span>
        </p>
      ))}
    </div>
  );
}

const YieldTrendChart = memo(function YieldTrendChart({ data }) {
  return (
    <Card padding="p-0" className="overflow-hidden">
      <div className="px-5 pt-5 pb-3">
        <h3 className="text-sm font-semibold text-slate-800">Yield Trend</h3>
        <p className="text-xs text-slate-400 mt-0.5">Monthly yield performance</p>
      </div>

      <div className="px-3 pb-4 h-52 chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <defs>
              <linearGradient id="yieldGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#16a34a" stopOpacity={0.25} />
                <stop offset="100%" stopColor="#16a34a" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#94a3b8' }} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#94a3b8' }} width={35} />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="yield_tph"
              stroke="#16a34a"
              fill="url(#yieldGrad)"
              strokeWidth={2.5}
              dot={{ r: 3, fill: 'white', stroke: '#16a34a', strokeWidth: 2 }}
              activeDot={{ r: 5, fill: '#16a34a', stroke: 'white', strokeWidth: 2 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
});

export default YieldTrendChart;
