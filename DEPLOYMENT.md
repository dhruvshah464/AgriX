# AgriX Production Deployment Guide

This guide outlines the production deployment architecture for the AgriX Intelligence Platform. AgriX is built with a modern, decoupled stack (Vite/React frontend, FastAPI backend, PostgreSQL database). 

## 1. Environment Secrets

Before deploying, ensure you have the following secrets ready:

- `VITE_API_BASE_URL` - Production URL of your FastAPI backend.
- `VITE_SUPABASE_URL` - Your Supabase project URL.
- `VITE_SUPABASE_ANON_KEY` - Your Supabase publishable anon key.
- `VITE_MAPBOX_TOKEN` - Mapbox API token for geospatial layers.
- `GROQ_API_KEY` - Your Groq API key for Llama 3.1 inference.
- `DATABASE_URL` - Production PostgreSQL connection string.

---

## 2. Frontend Deployment (Vercel)

Vercel is the recommended hosting platform for the Vite/React frontend due to its edge caching and seamless CI/CD.

### Configuration
We have already pushed a `vercel.json` file to the frontend directory which ensures React Router's client-side routing works without throwing 404 errors.

### Deployment Steps
1. Push your code to GitHub.
2. In the Vercel Dashboard, import the repository.
3. Under **Project Settings > General**:
   - Change **Root Directory** to `frontend/react_app`.
   - Framework Preset: `Vite`.
   - Build Command: `npm run build`.
   - Output Directory: `dist`.
4. Under **Environment Variables**:
   - Add all `VITE_*` variables.
5. Click **Deploy**.

---

## 3. Backend Deployment (Render / AWS)

The FastAPI backend is built to run asynchronously via Uvicorn. The easiest and most scalable way to deploy it is via **Render** or **AWS Elastic Beanstalk**.

### Using Render.com (Recommended)

1. Create a new **Web Service** on Render.
2. Connect the GitHub repository.
3. Set the **Root Directory** to `.` (the project root).
4. Set the **Environment** to `Python 3`.
5. Set the **Build Command**:
   ```bash
   pip install -r backend/requirements.txt
   ```
6. Set the **Start Command**:
   ```bash
   export PYTHONPATH=$PYTHONPATH:. && uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```
7. Add your Environment Variables:
   - `GROQ_API_KEY`
   - `DATABASE_URL`
   - `SUPABASE_JWT_SECRET`
8. Click **Create Web Service**.

### Dockerizing (Alternative)

If deploying to AWS ECS or a VPS, you can containerize the backend.

**Dockerfile**
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 4. Database Setup (Supabase)

1. **Authentication**: In your Supabase dashboard, go to Authentication > Policies and ensure your email templates and rate limits are configured for production traffic.
2. **PostgreSQL**: Ensure your connection pooling (PgBouncer) is enabled in Supabase if your FastAPI backend is expecting high concurrency. Use the pooled connection string (usually port `6543`) for `DATABASE_URL`.

## 5. Post-Deployment Verification

1. Verify the frontend loads the 3D Parallax interface without console errors.
2. Navigate to the `/login` route to verify the Vercel `rewrites` are functioning.
3. Once logged in, interact with the **AI Assistant** to verify the Groq API key is successfully mapped in the backend environment.
4. Load the **Map Insights** page to ensure the Mapbox token resolves and the GeoJSON payloads are fetched correctly from the FastAPI backend.
