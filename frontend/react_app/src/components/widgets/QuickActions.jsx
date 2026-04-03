import * as LucideIcons from 'lucide-react';
import Card from '../ui/Card';

const colorMap = {
  blue:  'bg-blue-50 text-blue-600 hover:bg-blue-100',
  green: 'bg-green-50 text-green-600 hover:bg-green-100',
  amber: 'bg-amber-50 text-amber-600 hover:bg-amber-100',
  teal:  'bg-teal-50 text-teal-600 hover:bg-teal-100',
};

export default function QuickActions({ actions }) {
  return (
    <Card padding="p-5">
      <h3 className="text-sm font-semibold text-slate-800 mb-4">Quick Actions</h3>
      <div className="grid grid-cols-2 gap-3">
        {actions.map((action) => {
          const Icon = LucideIcons[action.icon] || LucideIcons.Zap;
          const colors = colorMap[action.color] || colorMap.green;
          return (
            <button
              key={action.id}
              className={`flex flex-col items-center gap-2 py-4 px-3 rounded-xl transition-all duration-200 ${colors} active:scale-95`}
            >
              <Icon size={20} />
              <span className="text-xs font-medium">{action.label}</span>
            </button>
          );
        })}
      </div>
    </Card>
  );
}
