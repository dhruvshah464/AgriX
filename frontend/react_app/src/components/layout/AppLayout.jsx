import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import CommandPalette from '../features/CommandPalette';
import NotificationPanel from '../features/NotificationPanel';
import { useApp } from '../../context/AppContext';
import useKeyboard from '../../hooks/useKeyboard';

export default function AppLayout() {
  const { sidebarCollapsed } = useApp();

  useKeyboard();

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />

      <div
        className={`transition-all duration-300 ease-in-out ${
          sidebarCollapsed ? 'ml-[72px]' : 'ml-[260px]'
        }`}
      >
        <TopBar />

        <main className="p-6 max-w-[1400px]">
          <div className="page-enter">
            <Outlet />
          </div>
        </main>
      </div>

      {/* Overlays */}
      <CommandPalette />
      <NotificationPanel />
    </div>
  );
}
