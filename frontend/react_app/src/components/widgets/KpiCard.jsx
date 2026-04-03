import { useEffect, useRef, useState } from 'react';
import { TrendingUp, TrendingDown, Wheat, Droplets, IndianRupee, HeartPulse } from 'lucide-react';

const iconMap = { Wheat, Droplets, IndianRupee, HeartPulse };
const colorMap = {
  green: { bg: 'bg-green-50', icon: 'text-green-600', ring: 'ring-green-100' },
  blue:  { bg: 'bg-blue-50', icon: 'text-blue-600', ring: 'ring-blue-100' },
  amber: { bg: 'bg-amber-50', icon: 'text-amber-600', ring: 'ring-amber-100' },
  teal:  { bg: 'bg-teal-50', icon: 'text-teal-600', ring: 'ring-teal-100' },
};

function AnimatedNumber({ value, format, unit }) {
  const [display, setDisplay] = useState(0);
  const ref = useRef(null);

  useEffect(() => {
    const duration = 800;
    const start = performance.now();
    const startVal = 0;

    function tick(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(startVal + (value - startVal) * eased);
      if (progress < 1) ref.current = requestAnimationFrame(tick);
    }

    ref.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(ref.current);
  }, [value]);

  if (format === 'currency') {
    return <>{unit}{Math.round(display).toLocaleString('en-IN')}</>;
  }
  if (unit === '%') {
    return <>{display.toFixed(1)}{unit}</>;
  }
  return <>{display.toFixed(2)} {unit}</>;
}

export default function KpiCard({ label, value, unit, delta, icon, color = 'green', format, delay = 0 }) {
  const Icon = iconMap[icon] || Wheat;
  const colors = colorMap[color] || colorMap.green;
  const isPositive = delta >= 0;

  return (
    <div
      className="bg-white rounded-xl border border-slate-100 shadow-card hover:shadow-card-hover p-5 transition-all duration-300 hover:-translate-y-0.5 animate-fade-in-up"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm text-slate-500 font-medium">{label}</p>
          <p className="text-2xl font-bold text-slate-800 mt-2 tracking-tight">
            <AnimatedNumber value={value} format={format} unit={unit} />
          </p>
          <div className="flex items-center gap-1.5 mt-2">
            {isPositive ? (
              <TrendingUp size={14} className="text-green-600" />
            ) : (
              <TrendingDown size={14} className="text-rose-600" />
            )}
            <span className={`text-xs font-semibold ${isPositive ? 'text-green-600' : 'text-rose-600'}`}>
              {isPositive ? '+' : ''}{delta.toFixed(1)}%
            </span>
            <span className="text-xs text-slate-400">vs last month</span>
          </div>
        </div>
        <div className={`w-11 h-11 rounded-xl ${colors.bg} ring-4 ${colors.ring} flex items-center justify-center`}>
          <Icon size={20} className={colors.icon} />
        </div>
      </div>
    </div>
  );
}
