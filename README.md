<div align="center">

<img src="https://img.shields.io/badge/AgriX-OS%202.0-10b981?style=for-the-badge&logo=react&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Groq-AI%20Inference-f55036?style=for-the-badge&logo=groq&logoColor=white" />
<img src="https://img.shields.io/badge/Supabase-Auth-3ecf8e?style=for-the-badge&logo=supabase&logoColor=white" />

<br />
<br />

# 🌍 AgriX Intelligence Platform
### *The unified operating system for global agriculture.*

**AgriX** is an elite, production-grade SaaS platform designed to bring trillion-dollar technical infrastructure to precision agriculture. Harnessing the power of ultra-fast LLM inference, geospatial data mapping, and predictive machine learning, AgriX allows modern agricultural enterprises to manage millions of acres from a single, stunning, Apple-inspired interface.

---

</div>

## 🚀 The Vision

Agriculture is the backbone of human civilization, yet it operates largely on legacy software. **AgriX OS 2.0** completely re-imagines farm management. By combining a **vibrant, glassmorphic UI** with **deep ML analytics**, we bridge the gap between heavy data science and intuitive user experience. 

Whether you are plotting sub-meter resolution NDVI heatmaps or asking our RAG-powered Agronomy AI about soil nitrogen depletion, AgriX responds instantaneously.

## ⚡ Core Systems Architecture

AgriX is engineered on a modern, decoupled stack built for extreme performance and instantaneous reactivity.

| Layer | Technologies | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | React, Vite, Framer Motion, TailwindCSS, Recharts | Provides the cinematic 3D parallax landing page, bento-box dashboard layouts, and complex interactive charts. |
| **API Gateway** | FastAPI, Python 3.12, Uvicorn | High-performance asynchronous backend handling REST routes, ML inference pipelines, and token validation. |
| **AI & ML Engine** | Groq (`llama-3.1-8b-instant`), LangChain, FAISS | Blazing-fast conversational RAG assistant processing vast agronomy datasets with sub-second latency. |
| **Data & Auth** | PostgreSQL, Supabase Auth | Secure, magic-link and JWT-based authentication coupled with robust relational data storage. |
| **Geospatial** | Mapbox GL JS, GeoJSON | Real-time rendering of satellite-powered productivity and crop-health heatmaps. |

## 🧬 Key Features

### 1. **Interactive 3D Parallax Interface**
The entry point to AgriX isn't a static webpage—it's an interactive experience. Powered by `framer-motion` springs, the dashboard mockup tracks mouse movements, tilting in 3D space. The UI utilizes strict Apple-level design tokens, emerald gradients, and `backdrop-blur-xl` glassmorphism to establish immediate psychological trust.

### 2. **Agronomy AI Engine (Powered by Groq)**
Talk directly to your data. The RAG assistant queries scientific agronomy datasets and your live telemetry simultaneously. By leveraging the **Groq API**, the assistant circumvents traditional LLM bottlenecks, providing near-instantaneous `llama-3.1` inference. *(Includes an Offline Demo Cache fallback for resilient operation during quota limits).*

### 3. **Geospatial Intelligence**
Sub-meter resolution satellite imagery processed on the backend into dynamic GeoJSON payloads. The frontend utilizes Mapbox to render live NDVI (Normalized Difference Vegetation Index) health indices, rainfall heatmaps, and yield productivity circles.

### 4. **Actuarial Risk & Insurance Dashboard**
A sophisticated financial module featuring live AI Risk Analysis. Actuarial models project drought, pest, and flood probabilities across a 6-month timeline, visualizing the risk through multi-layered `recharts` Area gradients, alongside active multi-peril crop insurance policy tracking.

### 5. **Predictive Yield Lab**
Machine learning models ingest millions of data points (soil pH, nitrogen, temperature) to predict harvest outcomes with extreme accuracy. When deep models are untrainable locally, the system seamlessly falls back to advanced deterministic heuristics so the operator never sees a crash.

## 🔐 Security & Authentication

AgriX relies on an impenetrable **Supabase JWT architecture**.
- **Dual-Mode Login**: Users can securely access the platform via Passwordless Magic Links or standard Email/Password combinations (bypassing free-tier email rate limits).
- **Protected Routes**: The React router strictly gates the dashboard. Unauthenticated users cannot bypass the `AuthContext` wrapper.
- **Backend Verification**: The FastAPI backend employs a strict dependency injection (`get_current_user`) that verifies the `Authorization: Bearer <token>` against the Supabase HS256 JWT secret before any AI or ML endpoint is triggered. *(Dev-mode bypass enabled for rapid local testing).*

## 💻 Local Development Setup

To run the complete project locally:

**1. Clone the repository**
```bash
git clone https://github.com/dhruvshah464/agriX.git
cd agriX
```

**2. Start the FastAPI Backend**
```bash
source backend/local_venv/bin/activate
export PYTHONPATH=$PYTHONPATH:.
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

**3. Start the React Frontend**
```bash
cd frontend/react_app
npm install
npm run dev
```

**4. Environment Variables**
Ensure you have the `.env` file loaded in both the root directory and the frontend directory containing your `VITE_MAPBOX_TOKEN`, `GROQ_API_KEY`, and `SUPABASE` credentials.

---
<div align="center">
  <p><b>Designed and Engineered for the Future of Farming.</b></p>
</div>
