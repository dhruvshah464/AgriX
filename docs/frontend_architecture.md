# Frontend Architecture

Stack: React + Vite + TailwindCSS + Mapbox GL + Recharts

## Routing
- `/` Overview dashboard
- `/forecast` climate forecast analytics
- `/maps` geospatial productivity view
- `/assistant` AI assistant experience

## Core Client Modules
- `src/services/apiClient.js`: typed API interactions
- `src/maps/ProductivityMap.jsx`: Mapbox rendering of GeoJSON productivity data
- `src/components/charts/*`: charting modules
- `src/dashboards/KpiPanel.jsx`: KPI cards

## Styling
- Tailwind utility system with custom green/agri palette
- Design tokens in `tailwind.config.js`
