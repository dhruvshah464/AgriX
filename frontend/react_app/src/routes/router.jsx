import { createBrowserRouter } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import AppLayout from '../components/layout/AppLayout';

// Lazy-loaded pages
const DashboardPage = lazy(() => import('../pages/DashboardPage'));
const FieldsPage = lazy(() => import('../pages/FieldsPage'));
const TasksPage = lazy(() => import('../pages/TasksPage'));
const EquipmentPage = lazy(() => import('../pages/EquipmentPage'));
const PredictionPage = lazy(() => import('../pages/PredictionPage'));
const ForecastPage = lazy(() => import('../pages/ForecastPage'));
const MapInsightsPage = lazy(() => import('../pages/MapInsightsPage'));
const ReportsPage = lazy(() => import('../pages/ReportsPage'));
const AssistantPage = lazy(() => import('../pages/AssistantPage'));
const SettingsPage = lazy(() => import('../pages/SettingsPage'));
const NotFoundPage = lazy(() => import('../pages/NotFoundPage'));

function SuspenseWrapper({ children }) {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center py-32">
          <div className="flex flex-col items-center gap-3">
            <div className="w-8 h-8 border-2 border-green-200 border-t-green-600 rounded-full animate-spin" />
            <p className="text-sm text-slate-400">Loading...</p>
          </div>
        </div>
      }
    >
      {children}
    </Suspense>
  );
}

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    errorElement: <SuspenseWrapper><NotFoundPage /></SuspenseWrapper>,
    children: [
      { index: true, element: <SuspenseWrapper><DashboardPage /></SuspenseWrapper> },
      { path: 'fields', element: <SuspenseWrapper><FieldsPage /></SuspenseWrapper> },
      { path: 'tasks', element: <SuspenseWrapper><TasksPage /></SuspenseWrapper> },
      { path: 'equipment', element: <SuspenseWrapper><EquipmentPage /></SuspenseWrapper> },
      { path: 'predict', element: <SuspenseWrapper><PredictionPage /></SuspenseWrapper> },
      { path: 'forecast', element: <SuspenseWrapper><ForecastPage /></SuspenseWrapper> },
      { path: 'maps', element: <SuspenseWrapper><MapInsightsPage /></SuspenseWrapper> },
      { path: 'reports', element: <SuspenseWrapper><ReportsPage /></SuspenseWrapper> },
      { path: 'assistant', element: <SuspenseWrapper><AssistantPage /></SuspenseWrapper> },
      { path: 'settings', element: <SuspenseWrapper><SettingsPage /></SuspenseWrapper> },
      { path: '*', element: <SuspenseWrapper><NotFoundPage /></SuspenseWrapper> },
    ],
  },
]);
