import { useState } from 'react';
import { CheckCircle2, Circle, Clock, AlertCircle, Filter } from 'lucide-react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import { tasksData } from '../data/mockData';

const statusConfig = {
  'completed':   { icon: CheckCircle2, color: 'text-green-600', bg: 'bg-green-50', label: 'Completed' },
  'in-progress': { icon: Clock, color: 'text-amber-600', bg: 'bg-amber-50', label: 'In Progress' },
  'pending':     { icon: Circle, color: 'text-slate-400', bg: 'bg-slate-50', label: 'Pending' },
};

const priorityConfig = {
  critical: 'red',
  high: 'amber',
  medium: 'blue',
  low: 'slate',
};

export default function TasksPage() {
  const [statusFilter, setStatusFilter] = useState('all');
  const [tasks, setTasks] = useState(tasksData);

  const filtered = statusFilter === 'all'
    ? tasks
    : tasks.filter(t => t.status === statusFilter);

  const counts = {
    all: tasks.length,
    pending: tasks.filter(t => t.status === 'pending').length,
    'in-progress': tasks.filter(t => t.status === 'in-progress').length,
    completed: tasks.filter(t => t.status === 'completed').length,
  };

  const toggleStatus = (taskId) => {
    setTasks(prev => prev.map(t => {
      if (t.id !== taskId) return t;
      const order = ['pending', 'in-progress', 'completed'];
      const next = order[(order.indexOf(t.status) + 1) % order.length];
      return { ...t, status: next };
    }));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-800">Tasks</h1>
        <p className="text-sm text-slate-500 mt-0.5">Manage field operations and assignments</p>
      </div>

      {/* Status filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {Object.entries(counts).map(([key, count]) => (
          <button
            key={key}
            onClick={() => setStatusFilter(key)}
            className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-all ${
              statusFilter === key
                ? 'bg-green-600 text-white shadow-sm'
                : 'bg-white text-slate-600 border border-slate-200 hover:border-slate-300'
            }`}
          >
            {key === 'all' ? 'All' : statusConfig[key]?.label || key}
            <span className={`px-1.5 py-0.5 text-xs rounded-full ${
              statusFilter === key ? 'bg-green-700 text-green-100' : 'bg-slate-100 text-slate-500'
            }`}>
              {count}
            </span>
          </button>
        ))}
      </div>

      {/* Task list */}
      <Card padding="p-0">
        <div className="divide-y divide-slate-50">
          {filtered.map((task) => {
            const status = statusConfig[task.status] || statusConfig.pending;
            const StatusIcon = status.icon;
            return (
              <div
                key={task.id}
                className="flex items-center gap-4 px-5 py-4 hover:bg-slate-50/50 transition-colors"
              >
                <button
                  onClick={() => toggleStatus(task.id)}
                  className={`flex-shrink-0 ${status.color} hover:scale-110 transition-transform`}
                  title="Toggle status"
                >
                  <StatusIcon size={20} />
                </button>

                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-medium ${task.status === 'completed' ? 'text-slate-400 line-through' : 'text-slate-800'}`}>
                    {task.title}
                  </p>
                  <p className="text-xs text-slate-400 mt-0.5">{task.field} · {task.assignee}</p>
                </div>

                <Badge variant={priorityConfig[task.priority]} className="text-[10px]">
                  {task.priority}
                </Badge>

                <span className="text-xs text-slate-400 hidden sm:block w-20 text-right">
                  {new Date(task.due).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}
                </span>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
