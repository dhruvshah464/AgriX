# AgriX Authentication Guidelines

AgriX utilizes **Supabase** for secure, passwordless authentication (Magic Links). 

## Frontend Flow
1. User requests a magic link on the `/login` route.
2. Supabase sends an email. Upon clicking, the user is redirected back to the app with an access token.
3. The `AuthContext` captures the session and updates the application state.
4. The JWT is automatically attached to the `Authorization: Bearer <token>` header in `apiClient.js` interceptors.

## Backend Verification
All protected FastAPI endpoints use the `get_current_user` dependency from `app.api.deps`.
- This dependency decodes the JWT using the Supabase JWT Secret.
- If invalid or expired, a `401 Unauthorized` exception is raised.
- Decoded user UUIDs are matched against our local PostgreSQL `users` table to inject user metadata into the request context.
