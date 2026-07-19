# Chronica Backend: Render + Neon Deployment Guide

This document describes every deployment-related change made to the backend and the exact process for deploying the FastAPI API on Render with PostgreSQL hosted by Neon.

## 1. Final architecture

The production request path is:

```text
Browser
  -> Chronica frontend on Vercel
  -> Chronica FastAPI backend on Render
  -> Chronica PostgreSQL database on Neon
```

Render does not host the production database. It receives a `DATABASE_URL` environment variable and connects securely to the separate Neon PostgreSQL database.

## 2. Files changed and why

### `render.yaml`

A Render Blueprint was added at the repository root. It defines:

- A Python web service named `chronica-backend`.
- Render's free instance plan.
- The Singapore region, which is generally the closest available Render region for users in India.
- Python 3.11.9.
- Dependency installation using `requirements.txt`.
- An Alembic migration before every application start.
- Uvicorn binding to `0.0.0.0` and Render's dynamic `$PORT`.
- `/health` as Render's health-check endpoint.
- Automatic deployments after commits.
- Production environment variables.
- Dashboard prompts for the Neon database URL and allowed frontend origins.
- Automatic generation of a strong JWT signing secret by Render.

The effective start command is:

```bash
alembic -c alembic/alembic.ini upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The `-c alembic/alembic.ini` option is necessary because this repository keeps `alembic.ini` inside the `alembic` directory rather than at the project root. The `&&` ensures the API starts only after migrations complete successfully.

### `app/core/config.py`

The previous personal local password was removed. The development database fallback now uses:

```text
postgresql+psycopg://postgres:Admin%40123@localhost:5432/chronica_database
```

The password is `Admin@123`, but `@` is a reserved URL character. Therefore it must appear as `%40` inside a connection URL. Render overrides this local fallback with `DATABASE_URL` from its environment.

The JWT secret fallback was changed to an explicitly development-only value. Render generates a separate strong secret. A database password and a JWT secret serve different purposes and must not be treated as the same credential.

### `app/main.py`

Automatic `Base.metadata.create_all()` was removed from application startup. Database structure is now controlled only by Alembic migrations. This avoids schema drift and ensures Render reports migration failures instead of starting against a partially created database.

### `app/db/database.py`

SQLAlchemy now uses:

```python
pool_pre_ping=True
pool_recycle=300
```

`pool_pre_ping` verifies a pooled database connection before handing it to an API request. If Neon suspended compute or closed an idle connection, SQLAlchemy discards the stale connection and opens a valid one. `pool_recycle=300` refreshes older pooled connections after five minutes.

### `app/models/models.py`

The `GameResult` enum is explicitly stored using its lowercase values:

```text
win, loss, draw
```

This matches the existing initial Alembic migration. Without this mapping, SQLAlchemy can attempt to save uppercase Python enum names into a PostgreSQL enum that permits only lowercase values.

### `.env.example`

The example now demonstrates the `psycopg` SQLAlchemy driver, the requested local password, production-style debug settings, and the `%40` encoding requirement. This file is documentation only; Render does not automatically load it.

### `docker-compose.yml`

Local Docker PostgreSQL and Adminer credentials now use:

```text
Password: Admin@123
URL representation: Admin%40123
```

These Docker settings are for local development only and do not create or configure a Neon database.

### `Dockerfile`

The health check previously imported the third-party `requests` package, which is not in `requirements.txt`. It now uses Python's built-in `urllib.request`, so the container health check works without another dependency.

## 3. Security warning about the requested password

`Admin@123` is short and predictable. It is included because it was explicitly requested, but it is not recommended for a public production database. Anyone who obtains the Neon hostname and role name can attempt to guess it. A randomly generated password of at least 20 characters is much safer.

Never commit a real Neon connection string to GitHub. `.env` is already ignored by `.gitignore`. The safe locations for the real connection string are the Neon dashboard and Render environment-variable storage.

## 4. Prepare GitHub

Run these checks from the backend directory:

```powershell
git status
git check-ignore .env
```

The second command should print `.env`, confirming that Git will ignore it. Review all changes, commit them, and push the backend repository to GitHub. Render must be able to access that GitHub repository.

Example commands, after reviewing the changes:

```powershell
git add .env.example Dockerfile docker-compose.yml render.yaml RENDER_NEON_DEPLOYMENT.md app/core/config.py app/db/database.py app/main.py app/models/models.py
git commit -m "Prepare backend for Render and Neon deployment"
git push origin main
```

Do not run these commands blindly if the working tree contains unrelated work that should not be included in the same commit.

## 5. Create the Neon project

1. Sign in at `https://console.neon.tech/`.
2. Select **New project**.
3. Use a project name such as `chronica-production`.
4. Choose an AWS region close to Render's Singapore region when Neon offers one.
5. Keep the default database and owner role, or name the database `chronica_database`.
6. Finish project creation.
7. Open Neon's **SQL Editor** if the owner-role password needs to be changed to the requested value.
8. Run the following statement after replacing `neondb_owner` if the dashboard shows a different owner role:

```sql
ALTER ROLE neondb_owner WITH PASSWORD 'Admin@123';
```

9. If Neon does not permit changing that managed role's password, use the password generated by Neon. The password inside `DATABASE_URL` must always match the actual Neon role password; the application cannot override it.
10. Open **Connect** in Neon.
11. Select the database used above.
12. Select the owner role.
13. Enable the **Pooled connection** option. A pooled hostname normally contains `-pooler`.
14. Copy the complete connection string.

Neon may display something similar to:

```text
postgresql://neondb_owner:Admin%40123@ep-example-pooler.ap-southeast-1.aws.neon.tech/chronica_database?sslmode=require
```

Change only the scheme so SQLAlchemy explicitly selects the installed psycopg 3 driver:

```text
postgresql+psycopg://neondb_owner:Admin%40123@ep-example-pooler.ap-southeast-1.aws.neon.tech/chronica_database?sslmode=require
```

Keep `sslmode=require`. Do not add quotation marks when saving the value in Render.

## 6. Deploy with the Render Blueprint

1. Sign in at `https://dashboard.render.com/` using the GitHub account that can access the backend repository.
2. Select **New** and then **Blueprint**.
3. Connect the `Chronica-Backend` repository.
4. Render detects `render.yaml` and displays the `chronica-backend` service.
5. Enter the requested unsynced environment variables.

For `DATABASE_URL`, paste the modified pooled Neon URL:

```text
postgresql+psycopg://NEON_ROLE:Admin%40123@NEON_POOLED_HOST/NEON_DATABASE?sslmode=require
```

For `BACKEND_CORS_ORIGINS`, initially use local development plus the known production Vercel URL:

```json
["http://localhost:5173","https://YOUR-VERCEL-PROJECT.vercel.app"]
```

The value must be valid JSON: double quotes around every origin, square brackets around the list, and no trailing comma. Do not add a trailing slash to an origin.

6. Confirm Blueprint creation.
7. Render installs dependencies.
8. Render runs `alembic upgrade head`, creating the `users`, `chess_games`, and `alembic_version` objects in Neon.
9. Render starts Uvicorn using its assigned port.
10. Render polls `/health` until the service is healthy.

## 7. Manual Render setup alternative

If Blueprint deployment is unavailable, create **New -> Web Service** and use:

```text
Name: chronica-backend
Runtime: Python 3
Region: Singapore
Branch: main
Root directory: leave blank
Build command: pip install --upgrade pip && pip install -r requirements.txt
Start command: alembic -c alembic/alembic.ini upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health check path: /health
Instance type: Free
```

Add these environment variables:

```text
PYTHON_VERSION=3.11.9
DATABASE_URL=postgresql+psycopg://NEON_ROLE:Admin%40123@NEON_POOLED_HOST/NEON_DATABASE?sslmode=require
SECRET_KEY=<a long randomly generated value>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ENVIRONMENT=production
DEBUG=False
BACKEND_CORS_ORIGINS=["http://localhost:5173","https://YOUR-VERCEL-PROJECT.vercel.app"]
```

Generate a JWT secret locally if doing a manual deployment:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

The generated output belongs in `SECRET_KEY`; do not use `Admin@123` as the JWT signing secret.

## 8. Verify backend and database

After Render reports **Live**, replace the example host below with the assigned Render URL and open:

```text
https://chronica-backend.onrender.com/health
https://chronica-backend.onrender.com/api/docs
https://chronica-backend.onrender.com/api/openapi.json
```

The health response should resemble:

```json
{
  "status": "healthy",
  "environment": "production",
  "api_version": "1.0.0"
}
```

Open Neon's **Tables** view or SQL Editor and verify migrations:

```sql
SELECT version_num FROM alembic_version;
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

The migration version should be `001_initial`. The application tables should include `users` and `chess_games`.

Use Swagger at `/api/docs` to register a temporary user, log in, and create a chess game. Confirm the rows from Neon:

```sql
SELECT id, name, email, created_at FROM users;
SELECT id, user_id, title, result, created_at FROM chess_games;
```

Passwords stored in `users.password_hash` are application-user passwords hashed with bcrypt. They are unrelated to the Neon role password.

## 9. Connect the Vercel frontend

In the Vercel project, add this production environment variable:

```text
VITE_API_BASE_URL=https://YOUR-RENDER-SERVICE.onrender.com/api/v1
```

Redeploy the frontend because Vite embeds `VITE_*` variables during its build.

Copy the final Vercel production URL. In Render, edit `BACKEND_CORS_ORIGINS` so it contains that exact origin:

```json
["http://localhost:5173","https://chronica-frontend.vercel.app"]
```

Save the variable and redeploy/restart the Render service. Preview deployment URLs are different origins; add them explicitly only if they need API access.

## 10. Troubleshooting

### Render reports a database authentication error

The role, password, or host in `DATABASE_URL` is incorrect. Copy a fresh Neon connection string. If the password is `Admin@123`, ensure the URL contains `Admin%40123`, not an unescaped `@`.

### Render reports that it cannot load `psycopg`

Confirm `requirements.txt` contains `psycopg[binary]` and the URL begins with `postgresql+psycopg://`.

### Render cannot find Alembic configuration

Confirm the start command contains:

```text
alembic -c alembic/alembic.ini upgrade head
```

and that Render's root directory is the backend repository root.

### Migration says an object already exists

Do not delete tables immediately. This can mean tables were previously created without Alembic tracking. Back up the database first, inspect `alembic_version`, and reconcile the schema before retrying.

### Browser reports a CORS error

Check the browser's exact origin and add it to the JSON array in `BACKEND_CORS_ORIGINS`. The scheme (`https`), hostname, and port must match exactly. Redeploy after changing it.

### API works but the first request is slow

Render's free service can suspend after inactivity, and Neon can also suspend idle compute. The next request wakes them. This is expected on free plans.

### Render service starts but game creation fails

Inspect Render logs and confirm migration `001_initial` completed. Confirm the PostgreSQL `gameresult` enum contains lowercase `win`, `loss`, and `draw` values.

## 11. Production checklist

- The backend repository is pushed to GitHub.
- No `.env` file or real Neon URL is committed.
- Neon uses the intended database and role.
- The Render `DATABASE_URL` uses the pooled Neon hostname.
- The URL begins with `postgresql+psycopg://`.
- Special characters in the password are URL-encoded.
- `sslmode=require` remains present.
- Render generated or received a strong `SECRET_KEY`.
- `DEBUG` is `False`.
- `ENVIRONMENT` is `production`.
- `BACKEND_CORS_ORIGINS` contains the exact Vercel origin.
- Render's migration completed.
- `/health` responds successfully.
- `/api/docs` loads.
- Registration, login, and authenticated CRUD operations work.
- Records appear in Neon.
- The frontend uses the Render `/api/v1` URL and has been rebuilt on Vercel.

At that point, the backend is fully connected to Neon and ready to serve the Vercel frontend.
