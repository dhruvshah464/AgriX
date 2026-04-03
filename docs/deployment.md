# Deployment Configuration

## Docker Services
- `backend`: FastAPI backend
- `frontend`: Nginx-served React build
- `postgres`: relational store

## Run
```bash
cd docker
cp .env.example .env
docker compose up --build
```

## Service Endpoints
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Backend OpenAPI docs: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

## Production Notes
- Replace `.env.example` with environment-specific secret management.
- Use secret management for database and API keys.
- Add reverse proxy / TLS (Nginx, Traefik, or cloud gateway) for internet-facing deployments.
- Consider moving frontend and backend behind a single gateway domain for stricter CORS control.
