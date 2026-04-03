/* ─── Centralized Mock Data for AgriX Dashboard ─── */

export const kpiData = [
  { id: 'yield', label: 'Avg Yield', value: 4.12, unit: 't/ha', delta: 3.4, icon: 'Wheat', color: 'green' },
  { id: 'water', label: 'Water Efficiency', value: 71.8, unit: '%', delta: 1.9, icon: 'Droplets', color: 'blue' },
  { id: 'revenue', label: 'Projected Revenue', value: 1285000, unit: '₹', delta: 5.2, icon: 'IndianRupee', color: 'amber', format: 'currency' },
  { id: 'health', label: 'Crop Health Index', value: 87.3, unit: '%', delta: -0.8, icon: 'HeartPulse', color: 'teal' },
];

export const fieldsData = [
  { id: 'f1', name: 'North Meadow A1', area: 12.5, unit: 'acres', crop: 'Wheat', variety: 'HD-2967', health: 'excellent', healthScore: 94, growthStage: 'Grain Filling', daysToHarvest: 28, soilMoisture: 72, lastIrrigated: '2 hours ago', ndvi: 0.82 },
  { id: 'f2', name: 'East Valley B3', area: 8.2, unit: 'acres', crop: 'Rice', variety: 'Basmati 1121', health: 'good', healthScore: 78, growthStage: 'Tillering', daysToHarvest: 65, soilMoisture: 85, lastIrrigated: '30 min ago', ndvi: 0.71 },
  { id: 'f3', name: 'South Ridge C2', area: 15.0, unit: 'acres', crop: 'Cotton', variety: 'Bt Cotton', health: 'warning', healthScore: 62, growthStage: 'Flowering', daysToHarvest: 45, soilMoisture: 48, lastIrrigated: '1 day ago', ndvi: 0.58 },
  { id: 'f4', name: 'West Plains D1', area: 10.8, unit: 'acres', crop: 'Tomato', variety: 'Roma VF', health: 'excellent', healthScore: 91, growthStage: 'Fruiting', daysToHarvest: 18, soilMoisture: 68, lastIrrigated: '4 hours ago', ndvi: 0.79 },
  { id: 'f5', name: 'Central Block E4', area: 6.5, unit: 'acres', crop: 'Sugarcane', variety: 'Co-0238', health: 'good', healthScore: 75, growthStage: 'Grand Growth', daysToHarvest: 90, soilMoisture: 71, lastIrrigated: '6 hours ago', ndvi: 0.74 },
  { id: 'f6', name: 'River Side F2', area: 9.3, unit: 'acres', crop: 'Mustard', variety: 'Pusa Bold', health: 'critical', healthScore: 41, growthStage: 'Pod Formation', daysToHarvest: 22, soilMoisture: 32, lastIrrigated: '3 days ago', ndvi: 0.39 },
];

export const tasksData = [
  { id: 't1', title: 'Apply nitrogen fertilizer', field: 'North Meadow A1', priority: 'high', status: 'in-progress', due: '2026-04-04', assignee: 'Rajesh K.' },
  { id: 't2', title: 'Irrigation schedule check', field: 'East Valley B3', priority: 'medium', status: 'pending', due: '2026-04-04', assignee: 'Priya S.' },
  { id: 't3', title: 'Pest inspection round', field: 'South Ridge C2', priority: 'high', status: 'pending', due: '2026-04-05', assignee: 'Amit P.' },
  { id: 't4', title: 'Harvest preparation', field: 'West Plains D1', priority: 'medium', status: 'completed', due: '2026-04-03', assignee: 'Dhruv S.' },
  { id: 't5', title: 'Soil sampling for lab', field: 'Central Block E4', priority: 'low', status: 'pending', due: '2026-04-06', assignee: 'Neha R.' },
  { id: 't6', title: 'Drip line repair', field: 'River Side F2', priority: 'critical', status: 'in-progress', due: '2026-04-03', assignee: 'Vikram T.' },
  { id: 't7', title: 'Spray fungicide treatment', field: 'South Ridge C2', priority: 'high', status: 'pending', due: '2026-04-05', assignee: 'Amit P.' },
  { id: 't8', title: 'Equipment calibration', field: 'All Fields', priority: 'low', status: 'completed', due: '2026-04-02', assignee: 'Rajesh K.' },
];

export const equipmentData = [
  { id: 'e1', name: 'John Deere 5310', type: 'Tractor', status: 'operational', location: 'North Meadow A1', fuelLevel: 78, hoursUsed: 1240, nextService: '2026-04-15', image: '🚜' },
  { id: 'e2', name: 'Mahindra Jivo 245', type: 'Tractor', status: 'operational', location: 'shed', fuelLevel: 92, hoursUsed: 890, nextService: '2026-05-01', image: '🚜' },
  { id: 'e3', name: 'Drone Unit Alpha', type: 'Drone', status: 'charging', location: 'Control Room', batteryLevel: 45, flightHours: 120, nextService: '2026-04-20', image: '🛸' },
  { id: 'e4', name: 'Pump Station PS-01', type: 'Irrigation', status: 'active', location: 'East Valley B3', fuelLevel: null, hoursUsed: 3200, nextService: '2026-04-10', image: '💧' },
  { id: 'e5', name: 'Sprayer SP-200', type: 'Sprayer', status: 'maintenance', location: 'Workshop', fuelLevel: 35, hoursUsed: 560, nextService: '2026-04-03', image: '🔧' },
  { id: 'e6', name: 'Harvester H-500', type: 'Harvester', status: 'idle', location: 'Shed B', fuelLevel: 60, hoursUsed: 780, nextService: '2026-04-25', image: '🌾' },
];

export const weatherData = {
  current: { temp: 29, feelsLike: 31, condition: 'Partly Cloudy', humidity: 65, windSpeed: 12, windDir: 'NW', uvIndex: 6, visibility: 10 },
  forecast: [
    { day: 'Today', high: 32, low: 22, condition: 'Partly Cloudy', icon: '⛅', rain: 10 },
    { day: 'Fri', high: 34, low: 23, condition: 'Sunny', icon: '☀️', rain: 0 },
    { day: 'Sat', high: 30, low: 21, condition: 'Thunderstorm', icon: '⛈️', rain: 80 },
    { day: 'Sun', high: 28, low: 20, condition: 'Rainy', icon: '🌧️', rain: 65 },
    { day: 'Mon', high: 31, low: 22, condition: 'Partly Cloudy', icon: '⛅', rain: 15 },
  ],
};

export const growthChartData = [
  { week: 'W1', height: 12, biomass: 0.8, lai: 0.5 },
  { week: 'W2', height: 18, biomass: 1.2, lai: 0.9 },
  { week: 'W3', height: 28, biomass: 2.1, lai: 1.4 },
  { week: 'W4', height: 38, biomass: 3.2, lai: 2.0 },
  { week: 'W5', height: 52, biomass: 4.5, lai: 2.8 },
  { week: 'W6', height: 64, biomass: 5.8, lai: 3.4 },
  { week: 'W7', height: 72, biomass: 6.9, lai: 3.9 },
  { week: 'W8', height: 78, biomass: 7.6, lai: 4.2 },
  { week: 'W9', height: 82, biomass: 8.1, lai: 4.1 },
  { week: 'W10', height: 84, biomass: 8.4, lai: 3.8 },
];

export const yieldTrendData = [
  { month: 'Oct', yield_tph: 3.2 },
  { month: 'Nov', yield_tph: 3.5 },
  { month: 'Dec', yield_tph: 3.8 },
  { month: 'Jan', yield_tph: 4.0 },
  { month: 'Feb', yield_tph: 4.4 },
  { month: 'Mar', yield_tph: 4.6 },
  { month: 'Apr', yield_tph: 4.1 },
];

export const revenueData = [
  { month: 'Oct', revenue: 320000, expenses: 180000 },
  { month: 'Nov', revenue: 410000, expenses: 195000 },
  { month: 'Dec', revenue: 380000, expenses: 210000 },
  { month: 'Jan', revenue: 520000, expenses: 240000 },
  { month: 'Feb', revenue: 480000, expenses: 220000 },
  { month: 'Mar', revenue: 610000, expenses: 260000 },
];

export const aiInsights = [
  { id: 'ai1', type: 'recommendation', title: 'Optimize Irrigation Timing', description: 'Shifting irrigation to early morning (5-7 AM) could reduce water usage by 18% while maintaining soil moisture.', confidence: 92, impact: 'high', field: 'East Valley B3' },
  { id: 'ai2', type: 'alert', title: 'Pest Risk Detected', description: 'Cotton bollworm population trending upward in South Ridge. Recommend immediate scouting and preventive spray.', confidence: 87, impact: 'critical', field: 'South Ridge C2' },
  { id: 'ai3', type: 'forecast', title: 'Yield Prediction Update', description: 'Based on current growth patterns, wheat yield in A1 is projected at 4.8 t/ha — 12% above seasonal average.', confidence: 85, impact: 'positive', field: 'North Meadow A1' },
  { id: 'ai4', type: 'recommendation', title: 'Nutrient Deficiency Signal', description: 'Spectral analysis indicates potassium deficiency in mustard crop. Recommend foliar spray of KNO3 at 2% concentration.', confidence: 78, impact: 'medium', field: 'River Side F2' },
];

export const quickActionsData = [
  { id: 'qa1', label: 'Start Irrigation', icon: 'Droplets', color: 'blue' },
  { id: 'qa2', label: 'Log Observation', icon: 'Notebook', color: 'green' },
  { id: 'qa3', label: 'Schedule Task', icon: 'CalendarPlus', color: 'amber' },
  { id: 'qa4', label: 'Run AI Analysis', icon: 'Brain', color: 'teal' },
];

export const reportsData = {
  summary: {
    totalRevenue: 2720000,
    totalExpenses: 1305000,
    netProfit: 1415000,
    profitMargin: 52.0,
    totalYield: 156.8,
    avgYieldPerAcre: 2.52,
  },
  monthly: revenueData,
  topCrops: [
    { crop: 'Wheat', revenue: 980000, yield: 58.2, area: 12.5 },
    { crop: 'Rice', revenue: 720000, yield: 42.6, area: 8.2 },
    { crop: 'Tomato', revenue: 540000, yield: 28.4, area: 10.8 },
    { crop: 'Cotton', revenue: 480000, yield: 27.6, area: 15.0 },
  ],
};
