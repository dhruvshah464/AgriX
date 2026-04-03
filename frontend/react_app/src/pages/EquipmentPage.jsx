import { Fuel, Clock, Wrench, MapPin } from 'lucide-react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import { equipmentData } from '../data/mockData';

const statusConfig = {
  operational:  { variant: 'green', label: 'Operational' },
  active:       { variant: 'green', label: 'Active' },
  idle:         { variant: 'slate', label: 'Idle' },
  charging:     { variant: 'blue', label: 'Charging' },
  maintenance:  { variant: 'amber', label: 'Maintenance' },
};

export default function EquipmentPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-800">Equipment</h1>
        <p className="text-sm text-slate-500 mt-0.5">Track and manage farm assets</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {equipmentData.map((equip) => {
          const status = statusConfig[equip.status] || statusConfig.idle;
          const fuelOrBattery = equip.batteryLevel != null ? equip.batteryLevel : equip.fuelLevel;
          const fuelLabel = equip.batteryLevel != null ? 'Battery' : 'Fuel';

          return (
            <Card key={equip.id} className="hover:-translate-y-0.5">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{equip.image}</span>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-800">{equip.name}</h3>
                    <p className="text-xs text-slate-500">{equip.type}</p>
                  </div>
                </div>
                <Badge variant={status.variant} dot>{status.label}</Badge>
              </div>

              <div className="mt-4 space-y-3">
                {fuelOrBattery != null && (
                  <div>
                    <div className="flex items-center justify-between text-xs mb-1">
                      <span className="text-slate-500 flex items-center gap-1"><Fuel size={12} /> {fuelLabel}</span>
                      <span className="font-medium text-slate-700">{fuelOrBattery}%</span>
                    </div>
                    <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${
                          fuelOrBattery > 60 ? 'bg-green-500' : fuelOrBattery > 30 ? 'bg-amber-500' : 'bg-rose-500'
                        }`}
                        style={{ width: `${fuelOrBattery}%` }}
                      />
                    </div>
                  </div>
                )}

                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="flex items-center gap-1.5 text-slate-500">
                    <MapPin size={12} />
                    <span className="truncate">{equip.location}</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-slate-500">
                    <Clock size={12} />
                    <span>{equip.hoursUsed}h used</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                  <span className="text-slate-400 flex items-center gap-1">
                    <Wrench size={12} /> Next service
                  </span>
                  <span className="font-medium text-slate-600">
                    {new Date(equip.nextService).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}
                  </span>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
