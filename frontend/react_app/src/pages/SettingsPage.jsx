import { User, Bell, Palette, Shield, LogOut } from 'lucide-react';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import Avatar from '../components/ui/Avatar';
import { useApp } from '../context/AppContext';

export default function SettingsPage() {
  const { user } = useApp();

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-xl font-bold text-slate-800">Settings</h1>
        <p className="text-sm text-slate-500 mt-0.5">Manage your account and preferences</p>
      </div>

      {/* Profile */}
      <Card padding="p-6">
        <div className="flex items-center gap-2 mb-5">
          <User size={16} className="text-slate-600" />
          <h3 className="text-sm font-semibold text-slate-800">Profile</h3>
        </div>

        <div className="flex items-center gap-5 mb-6">
          <Avatar name={user.name} size="xl" color="green" />
          <div>
            <p className="font-semibold text-slate-800">{user.name}</p>
            <p className="text-sm text-slate-500">{user.role} · {user.farm}</p>
            <p className="text-xs text-slate-400">{user.email}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Input id="settings-name" label="Full Name" defaultValue={user.name} />
          <Input id="settings-email" label="Email" type="email" defaultValue={user.email} />
          <Input id="settings-role" label="Role" defaultValue={user.role} />
          <Input id="settings-farm" label="Farm Name" defaultValue={user.farm} />
        </div>

        <div className="mt-5">
          <Button icon={User}>Update Profile</Button>
        </div>
      </Card>

      {/* Notifications */}
      <Card padding="p-6">
        <div className="flex items-center gap-2 mb-5">
          <Bell size={16} className="text-slate-600" />
          <h3 className="text-sm font-semibold text-slate-800">Notifications</h3>
        </div>

        <div className="space-y-4">
          {[
            { label: 'Irrigation alerts', description: 'Get notified when fields need watering', checked: true },
            { label: 'Weather advisories', description: 'Severe weather and forecast updates', checked: true },
            { label: 'Task reminders', description: 'Upcoming and overdue task notifications', checked: false },
            { label: 'AI recommendations', description: 'New AI insights and suggestions', checked: true },
          ].map((item) => (
            <label key={item.label} className="flex items-center justify-between py-2 cursor-pointer group">
              <div>
                <p className="text-sm font-medium text-slate-700 group-hover:text-slate-800">{item.label}</p>
                <p className="text-xs text-slate-400">{item.description}</p>
              </div>
              <div className="relative">
                <input type="checkbox" defaultChecked={item.checked} className="sr-only peer" />
                <div className="w-10 h-6 bg-slate-200 rounded-full peer-checked:bg-green-500 transition-colors" />
                <div className="absolute left-0.5 top-0.5 w-5 h-5 bg-white rounded-full shadow-sm peer-checked:translate-x-4 transition-transform" />
              </div>
            </label>
          ))}
        </div>
      </Card>

      {/* Appearance */}
      <Card padding="p-6">
        <div className="flex items-center gap-2 mb-5">
          <Palette size={16} className="text-slate-600" />
          <h3 className="text-sm font-semibold text-slate-800">Appearance</h3>
        </div>

        <div className="flex gap-3">
          {[
            { label: 'Light', active: true, bg: 'bg-white border-2 border-green-500' },
            { label: 'Dark', active: false, bg: 'bg-slate-800 border-2 border-slate-300' },
            { label: 'System', active: false, bg: 'bg-gradient-to-r from-white to-slate-800 border-2 border-slate-300' },
          ].map((theme) => (
            <button
              key={theme.label}
              className={`flex flex-col items-center gap-2 p-3 rounded-xl transition-all ${
                theme.active ? 'ring-2 ring-green-500 ring-offset-2' : 'hover:bg-slate-50'
              }`}
            >
              <div className={`w-16 h-10 rounded-lg ${theme.bg}`} />
              <span className="text-xs font-medium text-slate-600">{theme.label}</span>
            </button>
          ))}
        </div>
      </Card>

      {/* Danger Zone */}
      <Card padding="p-6" className="border-rose-100">
        <div className="flex items-center gap-2 mb-3">
          <Shield size={16} className="text-rose-600" />
          <h3 className="text-sm font-semibold text-slate-800">Danger Zone</h3>
        </div>
        <p className="text-xs text-slate-500 mb-4">Once you sign out, you'll need to authenticate again.</p>
        <Button variant="danger" icon={LogOut}>Sign Out</Button>
      </Card>
    </div>
  );
}
