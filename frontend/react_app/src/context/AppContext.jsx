import { createContext, useContext, useReducer, useCallback } from 'react';

const AppContext = createContext(null);

const initialState = {
  sidebarCollapsed: false,
  commandPaletteOpen: false,
  notificationsOpen: false,
  notifications: [
    { id: 1, title: 'Irrigation Alert', message: 'Field B3 moisture level below threshold', type: 'warning', read: false, time: '5 min ago' },
    { id: 2, title: 'Harvest Ready', message: 'Wheat in Field A1 has reached maturity', type: 'success', read: false, time: '1 hour ago' },
    { id: 3, title: 'Weather Advisory', message: 'Heavy rainfall expected in 48 hours', type: 'info', read: true, time: '3 hours ago' },
    { id: 4, title: 'Equipment Maintenance', message: 'Tractor T-04 scheduled service due', type: 'warning', read: true, time: '1 day ago' },
  ],
  user: {
    name: 'Dhruv Shah',
    email: 'dhruv@agrix.farm',
    avatar: null,
    role: 'Farm Manager',
    farm: 'Green Valley Estates',
  },
};

function appReducer(state, action) {
  switch (action.type) {
    case 'TOGGLE_SIDEBAR':
      return { ...state, sidebarCollapsed: !state.sidebarCollapsed };
    case 'SET_SIDEBAR':
      return { ...state, sidebarCollapsed: action.payload };
    case 'TOGGLE_COMMAND_PALETTE':
      return { ...state, commandPaletteOpen: !state.commandPaletteOpen };
    case 'OPEN_COMMAND_PALETTE':
      return { ...state, commandPaletteOpen: true };
    case 'CLOSE_COMMAND_PALETTE':
      return { ...state, commandPaletteOpen: false };
    case 'TOGGLE_NOTIFICATIONS':
      return { ...state, notificationsOpen: !state.notificationsOpen };
    case 'CLOSE_NOTIFICATIONS':
      return { ...state, notificationsOpen: false };
    case 'MARK_NOTIFICATION_READ':
      return {
        ...state,
        notifications: state.notifications.map(n =>
          n.id === action.payload ? { ...n, read: true } : n
        ),
      };
    case 'MARK_ALL_READ':
      return {
        ...state,
        notifications: state.notifications.map(n => ({ ...n, read: true })),
      };
    default:
      return state;
  }
}

export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  const toggleSidebar = useCallback(() => dispatch({ type: 'TOGGLE_SIDEBAR' }), []);
  const setSidebar = useCallback((v) => dispatch({ type: 'SET_SIDEBAR', payload: v }), []);
  const toggleCommandPalette = useCallback(() => dispatch({ type: 'TOGGLE_COMMAND_PALETTE' }), []);
  const openCommandPalette = useCallback(() => dispatch({ type: 'OPEN_COMMAND_PALETTE' }), []);
  const closeCommandPalette = useCallback(() => dispatch({ type: 'CLOSE_COMMAND_PALETTE' }), []);
  const toggleNotifications = useCallback(() => dispatch({ type: 'TOGGLE_NOTIFICATIONS' }), []);
  const closeNotifications = useCallback(() => dispatch({ type: 'CLOSE_NOTIFICATIONS' }), []);
  const markNotificationRead = useCallback((id) => dispatch({ type: 'MARK_NOTIFICATION_READ', payload: id }), []);
  const markAllRead = useCallback(() => dispatch({ type: 'MARK_ALL_READ' }), []);

  const value = {
    ...state,
    toggleSidebar,
    setSidebar,
    toggleCommandPalette,
    openCommandPalette,
    closeCommandPalette,
    toggleNotifications,
    closeNotifications,
    markNotificationRead,
    markAllRead,
    unreadCount: state.notifications.filter(n => !n.read).length,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be used within AppProvider');
  return ctx;
}
