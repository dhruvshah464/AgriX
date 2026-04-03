import { NavLink, Outlet } from "react-router-dom";

const links = [
  { to: "/", label: "Overview" },
  { to: "/predict", label: "Yield Lab" },
  { to: "/forecast", label: "Forecast" },
  { to: "/maps", label: "Geospatial" },
  { to: "/assistant", label: "AI Assistant" },
];

export default function Layout() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_10%_20%,#f5faef_0%,#d8e9c7_35%,#dce0f2_100%)] text-leaf-800">
      <header className="border-b border-leaf-200/60 bg-white/70 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">AgriX</h1>
            <p className="text-sm text-leaf-600">AI-Powered Agricultural Intelligence Platform</p>
          </div>
          <nav className="flex gap-2">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `rounded-full px-4 py-2 text-sm font-medium transition ${
                    isActive ? "bg-leaf-700 text-white" : "bg-white text-leaf-700 hover:bg-leaf-100"
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-6 py-8">
        <Outlet />
      </main>
    </div>
  );
}
