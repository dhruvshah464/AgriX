import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export async function fetchSystemHealth() {
  const { data } = await apiClient.get("/system/health");
  return data;
}

export async function fetchYieldPrediction(payload) {
  const { data } = await apiClient.post("/predictions/yield", payload);
  return data;
}

export async function fetchCropRecommendation(payload) {
  const { data } = await apiClient.post("/predictions/recommendation", payload);
  return data;
}

export async function fetchClimateForecast(payload) {
  const { data } = await apiClient.post("/climate/forecast", payload);
  return data;
}

export async function fetchProductivityMap(payload) {
  const { data } = await apiClient.post("/geospatial/productivity-map", payload);
  return data;
}

export async function askAssistant(query) {
  const { data } = await apiClient.post("/assistant/query", { query });
  return data;
}
