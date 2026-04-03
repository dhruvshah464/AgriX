import { useState, useEffect, useRef, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Wheat, ClipboardList, Tractor, Beaker,
  CloudSun, Map, BarChart3, Bot, Settings, Search, ArrowRight
} from 'lucide-react';
import { useApp } from '../../context/AppContext';

const commands = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, path: '/', group: 'Pages' },
  { id: 'fields', label: 'My Fields', icon: Wheat, path: '/fields', group: 'Pages' },
  { id: 'tasks', label: 'Tasks', icon: ClipboardList, path: '/tasks', group: 'Pages' },
  { id: 'equipment', label: 'Equipment', icon: Tractor, path: '/equipment', group: 'Pages' },
  { id: 'predict', label: 'Yield Lab', icon: Beaker, path: '/predict', group: 'Pages' },
  { id: 'forecast', label: 'Climate Forecast', icon: CloudSun, path: '/forecast', group: 'Pages' },
  { id: 'maps', label: 'Geospatial', icon: Map, path: '/maps', group: 'Pages' },
  { id: 'reports', label: 'Reports', icon: BarChart3, path: '/reports', group: 'Pages' },
  { id: 'assistant', label: 'AI Assistant', icon: Bot, path: '/assistant', group: 'Pages' },
  { id: 'settings', label: 'Settings', icon: Settings, path: '/settings', group: 'Pages' },
];

export default function CommandPalette() {
  const { commandPaletteOpen, closeCommandPalette } = useApp();
  const [query, setQuery] = useState('');
  const [activeIndex, setActiveIndex] = useState(0);
  const inputRef = useRef(null);
  const navigate = useNavigate();

  const filtered = useMemo(() => {
    if (!query.trim()) return commands;
    const q = query.toLowerCase();
    return commands.filter(
      (cmd) => cmd.label.toLowerCase().includes(q) || cmd.group.toLowerCase().includes(q)
    );
  }, [query]);

  useEffect(() => {
    if (commandPaletteOpen) {
      setQuery('');
      setActiveIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [commandPaletteOpen]);

  useEffect(() => {
    setActiveIndex(0);
  }, [query]);

  if (!commandPaletteOpen) return null;

  const handleSelect = (cmd) => {
    if (cmd.path) navigate(cmd.path);
    if (cmd.action) cmd.action();
    closeCommandPalette();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveIndex((i) => Math.min(i + 1, filtered.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === 'Enter' && filtered[activeIndex]) {
      handleSelect(filtered[activeIndex]);
    }
  };

  const grouped = filtered.reduce((acc, cmd) => {
    if (!acc[cmd.group]) acc[cmd.group] = [];
    acc[cmd.group].push(cmd);
    return acc;
  }, {});

  let flatIndex = -1;

  return (
    <div className="cmd-overlay" onClick={closeCommandPalette}>
      <div className="cmd-dialog" onClick={(e) => e.stopPropagation()}>
        {/* Search Input */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-slate-100">
          <Search size={18} className="text-slate-400 flex-shrink-0" />
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search pages, actions..."
            className="flex-1 bg-transparent text-sm text-slate-800 placeholder:text-slate-400 outline-none"
            id="cmd-search-input"
          />
          <kbd className="px-1.5 py-0.5 bg-slate-100 border border-slate-200 rounded text-[10px] font-medium text-slate-400">
            ESC
          </kbd>
        </div>

        {/* Results */}
        <div className="max-h-80 overflow-y-auto py-2">
          {Object.entries(grouped).map(([group, items]) => (
            <div key={group}>
              <p className="px-4 py-1.5 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
                {group}
              </p>
              {items.map((cmd) => {
                flatIndex++;
                const idx = flatIndex;
                const Icon = cmd.icon;
                return (
                  <button
                    key={cmd.id}
                    onClick={() => handleSelect(cmd)}
                    className={`flex items-center gap-3 w-full px-4 py-2.5 text-sm transition-colors ${
                      idx === activeIndex
                        ? 'bg-green-50 text-green-700'
                        : 'text-slate-600 hover:bg-slate-50'
                    }`}
                    onMouseEnter={() => setActiveIndex(idx)}
                  >
                    <Icon size={16} className={idx === activeIndex ? 'text-green-600' : 'text-slate-400'} />
                    <span className="flex-1 text-left font-medium">{cmd.label}</span>
                    {idx === activeIndex && <ArrowRight size={14} className="text-green-500" />}
                  </button>
                );
              })}
            </div>
          ))}
          {filtered.length === 0 && (
            <p className="text-center text-sm text-slate-400 py-8">No results for "{query}"</p>
          )}
        </div>
      </div>
    </div>
  );
}
