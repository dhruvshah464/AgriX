import { Download, TrendingUp, Wallet, BarChart3, Wheat } from 'lucide-react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import RevenueChart from '../components/charts/RevenueChart';
import YieldTrendChart from '../components/charts/YieldTrendChart';
import { reportsData, yieldTrendData, revenueData } from '../data/mockData';

export default function ReportsPage() {
  const { summary, topCrops } = reportsData;

  const handleExport = () => {
    const csv = 'Crop,Revenue,Yield,Area\n' +
      topCrops.map(c => `${c.crop},${c.revenue},${c.yield},${c.area}`).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'agrix-report.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-slate-800">Reports</h1>
          <p className="text-sm text-slate-500 mt-0.5">Season analytics and performance summary</p>
        </div>
        <button onClick={handleExport} className="btn-secondary">
          <Download size={16} />
          Export CSV
        </button>
      </div>

      {/* Summary KPIs */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-green-50 flex items-center justify-center">
              <Wallet size={18} className="text-green-600" />
            </div>
            <div>
              <p className="text-xs text-slate-500">Total Revenue</p>
              <p className="text-lg font-bold text-slate-800">₹{(summary.totalRevenue / 100000).toFixed(1)}L</p>
            </div>
          </div>
        </Card>
        <Card>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-rose-50 flex items-center justify-center">
              <BarChart3 size={18} className="text-rose-600" />
            </div>
            <div>
              <p className="text-xs text-slate-500">Total Expenses</p>
              <p className="text-lg font-bold text-slate-800">₹{(summary.totalExpenses / 100000).toFixed(1)}L</p>
            </div>
          </div>
        </Card>
        <Card>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-50 flex items-center justify-center">
              <TrendingUp size={18} className="text-teal-600" />
            </div>
            <div>
              <p className="text-xs text-slate-500">Net Profit</p>
              <p className="text-lg font-bold text-green-700">₹{(summary.netProfit / 100000).toFixed(1)}L</p>
            </div>
          </div>
        </Card>
        <Card>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center">
              <Wheat size={18} className="text-amber-600" />
            </div>
            <div>
              <p className="text-xs text-slate-500">Total Yield</p>
              <p className="text-lg font-bold text-slate-800">{summary.totalYield} t</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RevenueChart data={revenueData} />
        <YieldTrendChart data={yieldTrendData} />
      </div>

      {/* Top Crops Table */}
      <Card padding="p-0">
        <div className="px-5 py-4 border-b border-slate-100">
          <h3 className="text-sm font-semibold text-slate-800">Top Performing Crops</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-100">
                <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Crop</th>
                <th className="text-right px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Revenue</th>
                <th className="text-right px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Yield</th>
                <th className="text-right px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Area</th>
                <th className="text-right px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">Yield/Acre</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {topCrops.map((crop) => (
                <tr key={crop.crop} className="hover:bg-slate-50/50 transition-colors">
                  <td className="px-5 py-3 font-medium text-slate-800 flex items-center gap-2">
                    <Wheat size={14} className="text-green-500" /> {crop.crop}
                  </td>
                  <td className="px-5 py-3 text-right text-slate-700">₹{crop.revenue.toLocaleString('en-IN')}</td>
                  <td className="px-5 py-3 text-right text-slate-700">{crop.yield} t</td>
                  <td className="px-5 py-3 text-right text-slate-600">{crop.area} acres</td>
                  <td className="px-5 py-3 text-right font-semibold text-green-600">{(crop.yield / crop.area).toFixed(2)} t/ac</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
