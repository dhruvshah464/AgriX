import Card from '../ui/Card';
import Badge from '../ui/Badge';

const priorityColors = {
  critical: 'red',
  high: 'amber',
  medium: 'blue',
  low: 'slate',
};

const statusConfig = {
  'completed':   { dot: 'bg-green-500', text: 'text-green-700' },
  'in-progress': { dot: 'bg-amber-500', text: 'text-amber-700' },
  'pending':     { dot: 'bg-slate-400', text: 'text-slate-600' },
};

export default function TaskCalendar({ tasks }) {
  // Group today's and upcoming tasks
  const today = new Date().toISOString().split('T')[0];
  const todayTasks = tasks.filter(t => t.due <= today && t.status !== 'completed');
  const upcomingTasks = tasks.filter(t => t.due > today).slice(0, 4);

  return (
    <Card padding="p-0" className="overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100">
        <h3 className="text-sm font-semibold text-slate-800">Upcoming Tasks</h3>
        <p className="text-xs text-slate-400 mt-0.5">{tasks.filter(t => t.status !== 'completed').length} pending</p>
      </div>

      <div className="divide-y divide-slate-50">
        {/* Today */}
        {todayTasks.length > 0 && (
          <>
            <p className="px-5 py-2 text-[10px] font-semibold text-slate-400 uppercase tracking-wider bg-slate-50/50">
              Today
            </p>
            {todayTasks.map((task) => (
              <TaskRow key={task.id} task={task} />
            ))}
          </>
        )}

        {/* Upcoming */}
        {upcomingTasks.length > 0 && (
          <>
            <p className="px-5 py-2 text-[10px] font-semibold text-slate-400 uppercase tracking-wider bg-slate-50/50">
              Upcoming
            </p>
            {upcomingTasks.map((task) => (
              <TaskRow key={task.id} task={task} />
            ))}
          </>
        )}
      </div>
    </Card>
  );
}

function TaskRow({ task }) {
  const priority = priorityColors[task.priority] || 'slate';
  const status = statusConfig[task.status] || statusConfig.pending;

  return (
    <div className="flex items-center gap-3 px-5 py-3 hover:bg-slate-50/50 transition-colors">
      <div className={`w-1.5 h-1.5 rounded-full ${status.dot} flex-shrink-0`} />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-slate-700 truncate">{task.title}</p>
        <p className="text-xs text-slate-400 truncate">{task.field} · {task.assignee}</p>
      </div>
      <Badge variant={priority} className="text-[10px]">{task.priority}</Badge>
    </div>
  );
}
