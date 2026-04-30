import axios from "axios";
import { supabase } from "../lib/supabase";


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

apiClient.interceptors.request.use(async (config) => {
  const { data: { session } } = await supabase.auth.getSession();
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`;
  }
  return config;
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
