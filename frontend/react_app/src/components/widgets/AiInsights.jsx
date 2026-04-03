import { Brain, AlertTriangle, TrendingUp, Lightbulb, ArrowRight } from 'lucide-react';
import Card from '../ui/Card';

const typeConfig = {
  recommendation: { icon: Lightbulb, color: 'text-amber-600', bg: 'bg-amber-50', ring: 'ring-amber-100', label: 'Recommendation' },
  alert:          { icon: AlertTriangle, color: 'text-rose-600', bg: 'bg-rose-50', ring: 'ring-rose-100', label: 'Alert' },
  forecast:       { icon: TrendingUp, color: 'text-green-600', bg: 'bg-green-50', ring: 'ring-green-100', label: 'Forecast' },
};

export default function AiInsights({ insights }) {
  return (
    <Card padding="p-0" className="overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center">
            <Brain size={16} className="text-white" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-800">AI Insights</h3>
            <p className="text-[10px] text-slate-400">Powered by AgriX Intelligence</p>
          </div>
        </div>
      </div>

      <div className="divide-y divide-slate-50">
        {insights.slice(0, 3).map((insight) => {
          const config = typeConfig[insight.type] || typeConfig.recommendation;
          const Icon = config.icon;

          return (
            <div key={insight.id} className="px-5 py-4 hover:bg-slate-50/50 transition-colors group cursor-pointer">
              <div className="flex gap-3">
                <div className={`w-8 h-8 rounded-lg ${config.bg} ring-2 ${config.ring} flex items-center justify-center flex-shrink-0 mt-0.5`}>
                  <Icon size={14} className={config.color} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`text-[10px] font-semibold uppercase tracking-wider ${config.color}`}>
                      {config.label}
                    </span>
                    <span className="text-[10px] text-slate-400">· {insight.confidence}% confidence</span>
                  </div>
                  <p className="text-sm font-medium text-slate-800">{insight.title}</p>
                  <p className="text-xs text-slate-500 mt-1 line-clamp-2">{insight.description}</p>
                  <p className="text-[10px] text-slate-400 mt-1.5 flex items-center gap-1">
                    📍 {insight.field}
                    <ArrowRight size={10} className="ml-auto opacity-0 group-hover:opacity-100 text-green-500 transition-opacity" />
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
