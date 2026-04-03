import { useState } from 'react';
import { Beaker, Sparkles, BarChart3, Wheat } from 'lucide-react';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import { fetchYieldPrediction, fetchCropRecommendation } from '../services/apiClient';

const initialForm = {
  farm_id: 'farm-001',
  season: 'kharif-2026',
  rainfall_mm: 160,
  temperature_c: 29,
  soil_ph: 6.5,
  nitrogen: 80,
  phosphorus: 45,
  potassium: 52,
};

const fields = [
  { key: 'farm_id', label: 'Farm ID', type: 'text' },
  { key: 'season', label: 'Season', type: 'text' },
  { key: 'rainfall_mm', label: 'Rainfall (mm)', type: 'number' },
  { key: 'temperature_c', label: 'Temperature (°C)', type: 'number' },
  { key: 'soil_ph', label: 'Soil pH', type: 'number', step: '0.1' },
  { key: 'nitrogen', label: 'Nitrogen (kg/ha)', type: 'number' },
  { key: 'phosphorus', label: 'Phosphorus (kg/ha)', type: 'number' },
  { key: 'potassium', label: 'Potassium (kg/ha)', type: 'number' },
];

export default function PredictionPage() {
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [yieldResult, setYieldResult] = useState(null);
  const [recommendationResult, setRecommendationResult] = useState(null);

  const onChange = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  const onSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      const payload = { ...form };
      ['rainfall_mm', 'temperature_c', 'soil_ph', 'nitrogen', 'phosphorus', 'potassium'].forEach(k => {
        payload[k] = Number(payload[k]);
      });
      const [yieldData, recData] = await Promise.all([
        fetchYieldPrediction(payload),
        fetchCropRecommendation(payload),
      ]);
      setYieldResult(yieldData);
      setRecommendationResult(recData);
    } catch {
      setError('Prediction service is currently unavailable. Check if the backend is running.');
      setYieldResult(null);
      setRecommendationResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
          <Beaker size={20} className="text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-slate-800">Yield Lab</h1>
          <p className="text-sm text-slate-500">AI-powered crop yield prediction & recommendation</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form */}
        <Card className="lg:col-span-2" padding="p-6">
          <form onSubmit={onSubmit} className="space-y-5">
            <div>
              <h3 className="text-sm font-semibold text-slate-800 mb-1">Input Parameters</h3>
              <p className="text-xs text-slate-400">Enter field conditions for yield estimation</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {fields.map((f) => (
                <Input
                  key={f.key}
                  id={`predict-${f.key}`}
                  label={f.label}
                  type={f.type}
                  step={f.step}
                  value={form[f.key]}
                  onChange={(e) => onChange(f.key, e.target.value)}
                />
              ))}
            </div>

            <Button type="submit" loading={loading} icon={Sparkles} className="w-full sm:w-auto">
              Predict Yield & Recommend Crop
            </Button>
          </form>
        </Card>

        {/* Results */}
        <div className="space-y-4">
          <Card>
            <div className="flex items-center gap-2 mb-3">
              <BarChart3 size={16} className="text-green-600" />
              <h3 className="text-sm font-semibold text-slate-800">Yield Prediction</h3>
            </div>
            {yieldResult ? (
              <div className="space-y-2">
                <p className="text-3xl font-bold text-green-700">{yieldResult.predicted_yield_tph} <span className="text-base font-normal text-slate-500">t/ha</span></p>
                <div className="flex items-center gap-2">
                  <Badge variant="green">{yieldResult.model_name}</Badge>
                  <Badge variant="blue">{(yieldResult.confidence * 100).toFixed(0)}% confidence</Badge>
                </div>
              </div>
            ) : (
              <p className="text-sm text-slate-400">Submit parameters to see yield forecast</p>
            )}
          </Card>

          <Card>
            <div className="flex items-center gap-2 mb-3">
              <Wheat size={16} className="text-amber-600" />
              <h3 className="text-sm font-semibold text-slate-800">Crop Recommendation</h3>
            </div>
            {recommendationResult ? (
              <div className="space-y-2">
                <p className="text-2xl font-bold text-amber-700 capitalize">{recommendationResult.recommended_crop}</p>
                <Badge variant="amber">{(recommendationResult.confidence * 100).toFixed(0)}% confidence</Badge>
              </div>
            ) : (
              <p className="text-sm text-slate-400">Recommendation appears after prediction</p>
            )}
          </Card>
        </div>
      </div>

      {error && (
        <div className="bg-rose-50 border border-rose-200 rounded-lg px-4 py-3 text-sm text-rose-700">
          {error}
        </div>
      )}
    </div>
  );
}
