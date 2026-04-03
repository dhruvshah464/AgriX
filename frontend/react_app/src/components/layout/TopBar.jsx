import { Search, Bell, Command } from 'lucide-react';
import { useApp } from '../../context/AppContext';
import Avatar from '../ui/Avatar';

export default function TopBar() {
  const { user, openCommandPalette, toggleNotifications, unreadCount } = useApp();

  const now = new Date();
  const hour = now.getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
  const dateStr = now.toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });

  return (
    <header
      className="sticky top-0 z-30 h-16 bg-white/80 backdrop-blur-xl border-b border-slate-100 flex items-center justify-between px-6"
      role="banner"
    >
      {/* Left: Greeting */}
      <div>
        <h2 className="text-sm font-semibold text-slate-800">
          {greeting}, <span className="text-green-700">{user.name.split(' ')[0]}</span>
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">{dateStr}</p>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-2">
        {/* Search trigger */}
        <button
          onClick={openCommandPalette}
          className="flex items-center gap-2 px-3 py-2 bg-slate-50 hover:bg-slate-100 rounded-lg text-sm text-slate-500 transition-colors duration-150 border border-slate-100"
          id="search-trigger"
          aria-label="Open command palette"
        >
          <Search size={15} className="text-slate-400" />
          <span className="hidden md:inline text-slate-400">Search...</span>
          <kbd className="hidden md:inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-white border border-slate-200 rounded text-[10px] font-medium text-slate-400 ml-4">
            <Command size={10} />K
          </kbd>
        </button>

        {/* Notifications */}
        <button
          onClick={toggleNotifications}
          className="relative btn-icon"
          id="notifications-trigger"
          aria-label={`Notifications${unreadCount > 0 ? `, ${unreadCount} unread` : ''}`}
        >
          <Bell size={20} />
          {unreadCount > 0 && <span className="notification-dot" />}
        </button>

        {/* User Avatar */}
        <div className="ml-1">
          <Avatar name={user.name} size="md" color="green" />
        </div>
      </div>
    </header>
  );
}
