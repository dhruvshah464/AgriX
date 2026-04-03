# <div align="center"><img src="https://raw.githubusercontent.com/lucide-react/lucide/main/icons/leaf.svg" width="48" height="48" /> <br/> AgriX Intelligence Platform</div>

<div align="center">
  <h3>Next-Generation AI for Precision Agriculture</h3>
  <p>A production-ready SaaS ecosystem transforming raw agricultural data into actionable intelligence.</p>

  [![Vite](https://img.shields.io/badge/Frontend-Vite%20%2B%20React-646CFF?style=for-the-badge&logo=vite)](https://vitejs.dev/)
  [![TailwindCSS](https://img.shields.io/badge/Styling-TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
  [![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![Python](https://img.shields.io/badge/ML-Python%203.9%2B-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
</div>

---

## 🛰️ System Overview

**AgriX** is an end-to-end intelligence platform that integrates satellite telemetry, weather forecasting, and machine learning to optimize global crop yields. Built with a focus on **visual excellence** and **data precision**, it provides a world-class experience for modern agronomists.

### 💎 Key Visual Pillars
- **Apple-Inspired Aesthetic:** Clean, light-minimal interface with glassmorphism and subtle micro-animations.
- **Data-First Design:** Interactive Recharts & Mapbox GL JS visualizations.
- **Intelligent Navigation:** Cmd+K Command Palette for lightning-fast workflow transitions.

---

## 🎨 Professional Dashboard

The heart of AgriX is a multi-layered dashboard designed for high-density information clarity.

![Dashboard Preview](file:///Users/shahdhruv/.gemini/antigravity/brain/e8030c43-62d3-4672-a8bc-480fc8f65667/dashboard_verification_1775223277837.png)

### 📊 Core Modules

| Module | Description | Technologies |
| :--- | :--- | :--- |
| **Yield Lab** | ML-driven yield prediction & crop optimization. | Scikit-learn, XGBoost |
| **Geospatial** | Satellite NDVI analysis & productivity heatmaps. | Mapbox GL, GeoPandas |
| **AI Assistant** | RAG-powered agronomy knowledge engine. | LangChain, FAISS |
| **Climate Hub** | High-precision weather impact forecasting. | ARIMA, Prophet |
| **Asset Manager** | Real-time fleet & task tracking. | React State Management |

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Frontend: Vite/React] -->|API Requests| B[Backend: FastAPI]
    B --> C[PostgreSQL / TimeScaleDB]
    B --> D[ML Inference Engine]
    B --> E[RAG / Vector Store]
    D --> F[Satellite & Sensor Data]
    E --> G[Knowledge Base]
    A -->|Cmd+K| H[Command Palette]
    A -->|Maps| I[Mapbox GL JS]
```

---

## 🚀 Advanced Features

### 🌾 Field & Crop Intelligence
Dynamic field cards provide real-time telemetry including soil moisture, NDVI health indices, and harvest countdowns.
![Fields View](file:///Users/shahdhruv/.gemini/antigravity/brain/e8030c43-62d3-4672-a8bc-480fc8f65667/my_fields_page_1775223331101.png)

### 🤖 RAG-Powered AI Assistant
Get expert agronomic advice instantly. Our AI parses through scientific datasets to provide contextualized answers for pest control, fertilization, and growth optimization.
![AI Assistant](file:///Users/shahdhruv/.gemini/antigravity/brain/e8030c43-62d3-4672-a8bc-480fc8f65667/ai_assistant_page_1775223376376.png)

### 📈 Financial & Predictive Analytics
Track seasonal ROI, revenue vs. expenses, and yield trends with production-grade data visualizations.
![Reports View](file:///Users/shahdhruv/.gemini/antigravity/brain/e8030c43-62d3-4672-a8bc-480fc8f65667/reports_page_1775223363929.png)

---

## 🛠️ Performance Features
- **HSL Design System:** Centralized color tokens for consistent styling.
- **Lazy Loading:** All pages are chunked and loaded on-demand for instant FCP.
- **Skeleton States:** Smooth loading transitions for all data-heavy widgets.
- **Error Boundaries:** Resilient UI that recovers gracefully from segment-level failures.

---

## 📡 Deployment & Scale
The system is containerized for cloud-scale deployment using **Docker Compose**.

```bash
# Spin up the entire intelligence stack
cd docker
docker compose up --build -d
```

---

<div align="center">
  <p>© 2026 AgriX Intelligence. Built for the future of food security.</p>
</div>
