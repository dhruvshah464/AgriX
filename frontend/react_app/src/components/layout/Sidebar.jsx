import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard, Map, Wheat, CloudSun, Bot, Settings,
  ChevronLeft, ChevronRight, Leaf, ClipboardList, Tractor, BarChart3,
  Beaker
} from 'lucide-react';
import { useApp } from '../../context/AppContext';

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/fields', label: 'My Fields', icon: Wheat },
  { to: '/tasks', label: 'Tasks', icon: ClipboardList },
  { to: '/equipment', label: 'Equipment', icon: Tractor },
  null, // divider
  { to: '/predict', label: 'Yield Lab', icon: Beaker },
  { to: '/forecast', label: 'Climate', icon: CloudSun },
  { to: '/maps', label: 'Geospatial', icon: Map },
  null, // divider
  { to: '/reports', label: 'Reports', icon: BarChart3 },
  { to: '/assistant', label: 'AI Assistant', icon: Bot },
];

const bottomItems = [
  { to: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
  const { sidebarCollapsed, toggleSidebar } = useApp();
  const location = useLocation();

  return (
    <aside
      className={`fixed left-0 top-0 bottom-0 z-40 flex flex-col bg-white border-r border-slate-100 shadow-sidebar transition-all duration-300 ease-in-out ${
        sidebarCollapsed ? 'w-[72px]' : 'w-[260px]'
      }`}
      aria-label="Main Navigation"
    >
      {/* Brand */}
      <div className={`flex items-center h-16 border-b border-slate-100 transition-all duration-300 ${sidebarCollapsed ? 'px-4 justify-center' : 'px-5'}`}>
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-sm flex-shrink-0">
            <Leaf size={18} className="text-white" />
          </div>
          {!sidebarCollapsed && (
            <div className="animate-fade-in">
              <h1 className="text-base font-bold text-slate-800 tracking-tight leading-none">AgriX</h1>
              <p className="text-[10px] text-slate-400 font-medium tracking-wider uppercase">Intelligence</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-0.5">
        {navItems.map((item, i) => {
          if (!item) {
            return <div key={`divider-${i}`} className="my-3 border-t border-slate-100" />;
          }
          const Icon = item.icon;
          const isActive = item.to === '/'
            ? location.pathname === '/'
            : location.pathname.startsWith(item.to);

          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 group ${
                isActive
                  ? 'bg-green-50 text-green-700 font-semibold'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-800'
              }`}
              title={sidebarCollapsed ? item.label : undefined}
            >
              <Icon
                size={20}
                className={`flex-shrink-0 transition-colors ${
                  isActive ? 'text-green-600' : 'text-slate-400 group-hover:text-slate-600'
                }`}
              />
              {!sidebarCollapsed && (
                <span className="sidebar-label">{item.label}</span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Bottom */}
      <div className="border-t border-slate-100 py-3 px-3 space-y-0.5">
        {bottomItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname.startsWith(item.to);
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 group ${
                isActive
                  ? 'bg-green-50 text-green-700'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-800'
              }`}
              title={sidebarCollapsed ? item.label : undefined}
            >
              <Icon
                size={20}
                className={`flex-shrink-0 ${isActive ? 'text-green-600' : 'text-slate-400 group-hover:text-slate-600'}`}
              />
              {!sidebarCollapsed && <span className="sidebar-label">{item.label}</span>}
            </NavLink>
          );
        })}

        {/* Collapse toggle */}
        <button
          onClick={toggleSidebar}
          className="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:bg-slate-50 hover:text-slate-700 transition-all duration-150"
          aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {sidebarCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
          {!sidebarCollapsed && <span>Collapse</span>}
        </button>
      </div>
    </aside>
  );
}
