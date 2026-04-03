import { useEffect, useRef } from 'react';
import { X, AlertTriangle, CheckCircle2, Info, Bell } from 'lucide-react';
import { useApp } from '../../context/AppContext';

const typeConfig = {
  warning: { icon: AlertTriangle, color: 'text-amber-500', bg: 'bg-amber-50' },
  success: { icon: CheckCircle2, color: 'text-green-500', bg: 'bg-green-50' },
  info:    { icon: Info, color: 'text-blue-500', bg: 'bg-blue-50' },
  error:   { icon: AlertTriangle, color: 'text-rose-500', bg: 'bg-rose-50' },
};

export default function NotificationPanel() {
  const { notificationsOpen, closeNotifications, notifications, markNotificationRead, markAllRead, unreadCount } = useApp();
  const panelRef = useRef(null);

  useEffect(() => {
    if (!notificationsOpen) return;
    function handleClick(e) {
      if (panelRef.current && !panelRef.current.contains(e.target) && !e.target.closest('#notifications-trigger')) {
        closeNotifications();
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [notificationsOpen, closeNotifications]);

  if (!notificationsOpen) return null;

  return (
    <div
      ref={panelRef}
      className="fixed top-16 right-6 w-96 bg-white rounded-xl border border-slate-100 shadow-lg z-50 animate-fade-in-down overflow-hidden"
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <Bell size={16} className="text-slate-600" />
          <h3 className="text-sm font-semibold text-slate-800">Notifications</h3>
          {unreadCount > 0 && (
            <span className="px-1.5 py-0.5 bg-green-100 text-green-700 text-[10px] font-bold rounded-full">
              {unreadCount}
            </span>
          )}
        </div>
        <div className="flex items-center gap-1">
          {unreadCount > 0 && (
            <button onClick={markAllRead} className="text-xs text-green-600 hover:text-green-700 font-medium px-2 py-1">
              Mark all read
            </button>
          )}
          <button onClick={closeNotifications} className="btn-icon w-7 h-7">
            <X size={16} />
          </button>
        </div>
      </div>

      {/* Notification list */}
      <div className="max-h-96 overflow-y-auto">
        {notifications.map((n) => {
          const config = typeConfig[n.type] || typeConfig.info;
          const Icon = config.icon;
          return (
            <button
              key={n.id}
              onClick={() => markNotificationRead(n.id)}
              className={`flex gap-3 w-full px-4 py-3 text-left transition-colors hover:bg-slate-50 border-b border-slate-50 ${
                !n.read ? 'bg-green-50/30' : ''
              }`}
            >
              <div className={`w-8 h-8 rounded-lg ${config.bg} flex items-center justify-center flex-shrink-0`}>
                <Icon size={15} className={config.color} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <p className={`text-sm font-medium truncate ${!n.read ? 'text-slate-800' : 'text-slate-600'}`}>
                    {n.title}
                  </p>
                  {!n.read && <span className="w-1.5 h-1.5 rounded-full bg-green-500 flex-shrink-0" />}
                </div>
                <p className="text-xs text-slate-500 mt-0.5 line-clamp-2">{n.message}</p>
                <p className="text-[10px] text-slate-400 mt-1">{n.time}</p>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
