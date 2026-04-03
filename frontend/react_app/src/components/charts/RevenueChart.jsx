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
          {entry.name}: <span className="font-semibold">₹{Number(entry.value).toLocaleString('en-IN')}</span>
        </p>
      ))}
    </div>
  );
}

const RevenueChart = memo(function RevenueChart({ data }) {
  return (
    <Card padding="p-0" className="overflow-hidden">
      <div className="px-5 pt-5 pb-3">
        <h3 className="text-sm font-semibold text-slate-800">Revenue vs Expenses</h3>
        <p className="text-xs text-slate-400 mt-0.5">Monthly financial summary</p>
      </div>

      <div className="px-3 pb-4 h-64 chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis
              dataKey="month"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: '#94a3b8' }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: '#94a3b8' }}
              tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`}
              width={45}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              iconType="circle"
              iconSize={8}
              wrapperStyle={{ fontSize: '11px', color: '#64748b', paddingTop: '8px' }}
            />
            <Bar
              dataKey="revenue"
              name="Revenue"
              fill="#16a34a"
              radius={[4, 4, 0, 0]}
              barSize={20}
              animationDuration={500}
            />
            <Bar
              dataKey="expenses"
              name="Expenses"
              fill="#e2e8f0"
              radius={[4, 4, 0, 0]}
              barSize={20}
              animationDuration={500}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
});

export default RevenueChart;
