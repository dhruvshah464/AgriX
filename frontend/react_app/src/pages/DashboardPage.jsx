import ErrorBoundary from '../components/ui/ErrorBoundary';
import KpiCard from '../components/widgets/KpiCard';
import FieldHero from '../components/widgets/FieldHero';
import WeatherWidget from '../components/widgets/WeatherWidget';
import TaskCalendar from '../components/widgets/TaskCalendar';
import GrowthChart from '../components/charts/GrowthChart';
import RevenueChart from '../components/charts/RevenueChart';
import AiInsights from '../components/widgets/AiInsights';
import QuickActions from '../components/widgets/QuickActions';
import {
  kpiData, fieldsData, weatherData, tasksData,
  growthChartData, revenueData, aiInsights, quickActionsData
} from '../data/mockData';

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <ErrorBoundary title="KPI cards failed to load">
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="kpi-section">
          {kpiData.map((kpi, i) => (
            <KpiCard key={kpi.id} {...kpi} delay={i * 80} />
          ))}
        </section>
      </ErrorBoundary>

      {/* Main content grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column (2/3) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Field Hero */}
          <ErrorBoundary title="Field overview failed">
            <section id="field-hero-section">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-base font-semibold text-slate-800">Fields Overview</h2>
                  <p className="text-xs text-slate-400">{fieldsData.length} active fields</p>
                </div>
                <a href="/fields" className="text-xs font-medium text-green-600 hover:text-green-700 transition-colors">
                  View All →
                </a>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {fieldsData.slice(0, 2).map((field, i) => (
                  <FieldHero key={field.id} field={field} index={i} />
                ))}
              </div>
            </section>
          </ErrorBoundary>

          {/* Growth Chart */}
          <ErrorBoundary title="Chart failed to load">
            <GrowthChart data={growthChartData} />
          </ErrorBoundary>

          {/* Revenue Chart */}
          <ErrorBoundary title="Revenue chart failed">
            <RevenueChart data={revenueData} />
          </ErrorBoundary>
        </div>

        {/* Right column (1/3) */}
        <div className="space-y-6">
          {/* Weather */}
          <ErrorBoundary title="Weather failed to load">
            <WeatherWidget weather={weatherData} />
          </ErrorBoundary>

          {/* Quick Actions */}
          <ErrorBoundary title="Actions failed">
            <QuickActions actions={quickActionsData} />
          </ErrorBoundary>

          {/* Task Calendar */}
          <ErrorBoundary title="Tasks failed to load">
            <TaskCalendar tasks={tasksData} />
          </ErrorBoundary>

          {/* AI Insights */}
          <ErrorBoundary title="AI Insights failed">
            <AiInsights insights={aiInsights} />
          </ErrorBoundary>
        </div>
      </div>
    </div>
  );
}
