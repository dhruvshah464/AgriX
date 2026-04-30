# Security & Production Readiness

## API Keys
- Never commit `.env` files. 
- The `VITE_SUPABASE_ANON_KEY` is meant to be public, but should be restricted by domain in the Supabase Dashboard before production.
- Backend secrets (`OPENAI_API_KEY`, `SUPABASE_JWT_SECRET`, `DATABASE_URL`) must never be exposed to the frontend.

## Network Resilience
- The frontend implements automatic retries for transient 5xx errors (configurable via Axios interceptors).
- The backend utilizes FastAPI's robust asynchronous I/O and should be placed behind a rate-limiting proxy (like NGINX or Cloudflare) to prevent abuse of heavy ML inference endpoints.
- Error Boundaries in the React application prevent crashes in a single widget from taking down the entire dashboard.
