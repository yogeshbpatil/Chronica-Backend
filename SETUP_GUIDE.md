# Chronica Backend - Complete Setup Guide

This guide will walk you through setting up the FastAPI backend for Chronica.

## ✅ Checklist

- [ ] PostgreSQL installed and running
- [ ] Python 3.10+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] Database created in PostgreSQL
- [ ] Migrations applied
- [ ] Server started successfully

## Step 1: Install PostgreSQL

### Windows

1. Download PostgreSQL installer from https://www.postgresql.org/download/windows/
2. Run the installer
3. Remember the password you set for the `postgres` user
4. Keep the default port (5432)

### macOS

```bash
brew install postgresql
brew services start postgresql
```

### Linux

```bash
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

## Step 2: Create Database

Open PostgreSQL command line (psql) and run:

```sql
-- Create database
CREATE DATABASE "Chronica_Database";

-- Create user (optional, if using separate user)
CREATE USER chronica_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE "Chronica_Database" TO chronica_user;
```

**Note:** If using the `postgres` default user, you can skip the user creation.

## Step 3: Clone and Setup Project

```bash
# Navigate to project directory
cd Chronica-Backend

# On Windows, run:
setup.bat

# On macOS/Linux, run:
chmod +x setup.sh
./setup.sh

# OR manually:
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

Edit `.env` file with your PostgreSQL credentials:

```env
# Example for local PostgreSQL with postgres user
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/Chronica_Database

# Example for separate user
DATABASE_URL=postgresql://chronica_user:your_secure_password@localhost:5432/Chronica_Database

# Keep other variables as default for development
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
API_TITLE=Chronica API
API_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True
BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

## Step 5: Apply Database Migrations

The database schema will be created when you start the server (auto-create from models).

Alternatively, if you want to use Alembic migrations:

```bash
# Apply migrations
alembic upgrade head

# If you need to generate migrations from model changes:
# alembic revision --autogenerate -m "describe your changes"
```

## Step 6: Start Development Server

```bash
# Make sure virtual environment is activated
python -m app.main

# OR using Uvicorn directly with reload:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [1234]
INFO:     Application startup complete
```

## Step 7: Test the API

### Using Swagger UI

Visit: **http://localhost:8000/api/docs**

You'll see an interactive API documentation where you can test all endpoints.

### Using curl

```bash
# Register a user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "TestPassword123"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'

# Use the token from login response in subsequent requests
# Get all games (replace TOKEN with your actual token)
curl -X GET "http://localhost:8000/api/v1/chess-games" \
  -H "Authorization: Bearer TOKEN"

# Create a game
curl -X POST "http://localhost:8000/api/v1/chess-games" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Game",
    "opponent": "Test Opponent",
    "result": "win",
    "opening": "Sicilian Defense",
    "notes": "Great game!"
  }'
```

## Troubleshooting

### PostgreSQL Connection Error

```
Error: could not connect to database server: Connection refused
```

**Solution:**

1. Check if PostgreSQL is running: `psql --version` should work
2. Verify DATABASE_URL in .env
3. Restart PostgreSQL service

### Database Does Not Exist

```
database "Chronica_Database" does not exist
```

**Solution:**
Run the SQL commands from Step 2 in psql to create the database.

### ModuleNotFoundError: No module named 'app'

```
ModuleNotFoundError: No module named 'app'
```

**Solution:**

1. Make sure you're in the project root directory
2. Virtual environment is activated
3. All dependencies are installed: `pip install -r requirements.txt`

### Port 8000 Already in Use

```
Address already in use
```

**Solution:**

```bash
# Use a different port
uvicorn app.main:app --port 8001

# Or kill process on port 8000 (macOS/Linux)
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

## Testing the API

### Test Workflow

1. **Register User**
   - Endpoint: `POST /api/v1/auth/register`
   - Body: name, email, password
   - Response: user info + JWT token

2. **Login**
   - Endpoint: `POST /api/v1/auth/login`
   - Body: email, password
   - Response: user info + JWT token (same format as register)

3. **Create Chess Game**
   - Endpoint: `POST /api/v1/chess-games`
   - Headers: `Authorization: Bearer {token}`
   - Body: title, opponent, result, opening, notes
   - Response: created game with ID

4. **List Games**
   - Endpoint: `GET /api/v1/chess-games`
   - Headers: `Authorization: Bearer {token}`
   - Response: all games for the user

5. **Get Game Stats**
   - Endpoint: `GET /api/v1/chess-games/stats`
   - Headers: `Authorization: Bearer {token}`
   - Response: total wins, losses, draws, win rate

## Environment for Frontend

Configure your Vue frontend's `.env` file:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

This tells the frontend to connect to your FastAPI backend.

## Next Steps

1. ✅ Backend is running locally
2. Start your Vue frontend: `npm run dev` in Chronica-Frontend
3. Test integration between frontend and backend
4. When ready to deploy:
   - Deploy backend on Render
   - Deploy database on Neon
   - Update CORS origins for production

## Common Commands

```bash
# View logs
uvicorn app.main:app --reload --log-level debug

# Check database connection
python -c "from app.db import engine; engine.connect(); print('✅ Database connected')"

# Reset database (careful!)
# Delete all tables and recreate them
# Or drop and recreate the database in PostgreSQL

# Create new migration
alembic revision --autogenerate -m "Your migration message"

# Apply latest migration
alembic upgrade head

# Revert last migration
alembic downgrade -1

# View migration history
alembic history
```

## Health Check

Visit: **http://localhost:8000/health**

Should return:

```json
{
  "status": "healthy",
  "environment": "development",
  "api_version": "1.0.0"
}
```

## Support

For issues or questions:

1. Check the README.md
2. Review error messages carefully
3. Check PostgreSQL is running
4. Ensure .env variables are correct
5. Try restarting the server

Happy coding! 🚀
