# Chronica Backend - FastAPI

A world-class FastAPI backend for the Chronica personal knowledge management platform.

## Features

- ✅ **User Authentication** - Register, login with JWT tokens
- ✅ **Chess Games CRUD** - Full create, read, update, delete operations
- ✅ **PostgreSQL Database** - Production-ready relational database
- ✅ **Swagger API Documentation** - Interactive API docs at `/api/docs`
- ✅ **Database Migrations** - Alembic for schema management
- ✅ **Type Safety** - Full TypeScript-style type hints with Pydantic
- ✅ **Security** - Password hashing with bcrypt, JWT authentication
- ✅ **CORS Support** - Configured for frontend integration
- ✅ **World-Class Architecture** - Following enterprise software standards

## Project Structure

```
Chronica-Backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py          # Authentication endpoints
│   │           └── chess_games.py   # Chess games CRUD endpoints
│   ├── core/
│   │   ├── config.py                # Configuration management
│   │   └── security.py              # Password & JWT utilities
│   ├── db/
│   │   └── database.py              # Database session management
│   ├── models/
│   │   └── models.py                # SQLAlchemy ORM models
│   ├── schemas/
│   │   ├── auth.py                  # Pydantic auth schemas
│   │   └── chess_game.py            # Pydantic game schemas
│   ├── services/
│   │   ├── auth.py                  # Authentication business logic
│   │   └── chess_game.py            # Chess games business logic
│   ├── utils/
│   │   └── dependencies.py          # FastAPI dependencies
│   └── main.py                      # FastAPI app factory
├── alembic/
│   ├── versions/                    # Database migration files
│   ├── env.py                       # Alembic environment config
│   └── alembic.ini                  # Alembic configuration
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
└── README.md                        # This file
```

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Setup Instructions

### 1. Create PostgreSQL Database

```sql
-- Connect to PostgreSQL and create database
CREATE DATABASE "Chronica_Database";
```

### 2. Clone & Install Dependencies

```bash
# Navigate to project directory
cd Chronica-Backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Most importantly, set DATABASE_URL:
# DATABASE_URL=postgresql://username:password@localhost:5432/Chronica_Database
```

### 4. Run Database Migrations

```bash
# Initialize Alembic (if needed)
# alembic init alembic

# Create initial migration (auto-detect models)
# alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

Or use the provided initial migration:

```bash
alembic upgrade head
```

### 5. Start Development Server

```bash
# Run the FastAPI server
python -m app.main

# Or use uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: **http://localhost:8000**

## API Documentation

### Swagger UI

Visit **http://localhost:8000/api/docs** for interactive API documentation.

### ReDoc

Visit **http://localhost:8000/api/redoc** for alternative documentation.

## Available Endpoints

### Authentication

| Method | Path                    | Description       |
| ------ | ----------------------- | ----------------- |
| POST   | `/api/v1/auth/register` | Register new user |
| POST   | `/api/v1/auth/login`    | Login user        |
| POST   | `/api/v1/auth/logout`   | Logout user       |

### Chess Games

| Method | Path                         | Description         |
| ------ | ---------------------------- | ------------------- |
| GET    | `/api/v1/chess-games`        | List all games      |
| POST   | `/api/v1/chess-games`        | Create new game     |
| GET    | `/api/v1/chess-games/stats`  | Get game statistics |
| GET    | `/api/v1/chess-games/recent` | Get recent games    |
| GET    | `/api/v1/chess-games/{id}`   | Get single game     |
| PATCH  | `/api/v1/chess-games/{id}`   | Update game         |
| DELETE | `/api/v1/chess-games/{id}`   | Delete game         |

## Environment Configuration

Create a `.env` file based on `.env.example`:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/Chronica_Database

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# API
API_TITLE=Chronica API
API_VERSION=1.0.0
API_DESCRIPTION=Personal Knowledge Management Platform Backend

# Environment
ENVIRONMENT=development
DEBUG=True

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

## Database Schema

### Users Table

- `id` (UUID) - Primary key
- `name` (String) - User's full name
- `email` (String) - Unique email address
- `password_hash` (String) - Bcrypt hashed password
- `created_at` (DateTime) - Account creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### Chess Games Table

- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key to users
- `title` (String) - Game title
- `opponent` (String) - Opponent name
- `result` (Enum) - win/loss/draw
- `opening` (String) - Chess opening name
- `notes` (Text) - Game analysis
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

## API Request/Response Examples

### Register User

**Request:**

```json
POST /api/v1/auth/register
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

**Response:**

```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2026-05-17T10:30:00"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2026-05-24T10:30:00"
}
```

### Create Chess Game

**Request:**

```json
POST /api/v1/chess-games
Authorization: Bearer <token>

{
  "title": "Tournament Round 3",
  "opponent": "Magnus Carlsen",
  "result": "win",
  "opening": "Sicilian Defense",
  "notes": "Good preparation in the opening"
}
```

**Response:**

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440111",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Tournament Round 3",
  "opponent": "Magnus Carlsen",
  "result": "win",
  "opening": "Sicilian Defense",
  "notes": "Good preparation in the opening",
  "created_at": "2026-05-17T10:35:00",
  "updated_at": "2026-05-17T10:35:00"
}
```

## Deployment

### Deploy on Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Set environment variables
4. Deploy

### Deploy Database on Neon

1. Create PostgreSQL database on Neon
2. Update `DATABASE_URL` in environment variables
3. Run migrations on deployed server

## Development Guide

### Adding a New Feature

1. **Create Model** in `app/models/models.py`
2. **Create Schemas** in `app/schemas/`
3. **Create Service** in `app/services/`
4. **Create Endpoints** in `app/api/v1/endpoints/`
5. **Create Migration** with `alembic revision --autogenerate -m "message"`
6. **Test with Swagger** at `/api/docs`

### Code Style

- Use type hints everywhere
- Follow PEP 8 conventions
- Use descriptive docstrings
- Keep functions focused and small

## Security Considerations

- ✅ Passwords hashed with bcrypt (cost factor: 12)
- ✅ JWT tokens expire after 7 days
- ✅ Bearer token authentication on protected routes
- ⚠️ Change `SECRET_KEY` in production
- ⚠️ Use HTTPS in production
- ⚠️ Set `DEBUG=False` in production

## Common Issues

### Database Connection Error

```
sqlalchemy.exc.ArgumentError: Could not parse rfc1738 URL
```

**Solution:** Check `DATABASE_URL` format in `.env`

### Migration Error

```
ModuleNotFoundError: No module named 'app'
```

**Solution:** Ensure project root is in Python path or run from project root

## Future Features

The following features are planned for future implementation:

- [ ] Diary CRUD
- [ ] Holiday management
- [ ] Notes system
- [ ] Analytics dashboard
- [ ] File upload support
- [ ] User profile management
- [ ] Search functionality
- [ ] Rate limiting
- [ ] Caching with Redis

## API Response Format

All responses follow a consistent format:

**Success (2xx)**:

```json
{
  "data": {},
  "message": "Operation successful"
}
```

**Error (4xx/5xx)**:

```json
{
  "detail": "Error message",
  "status": 400
}
```

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --port 8001
```

### Database Permission Error

```bash
# Check PostgreSQL user permissions
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE \"Chronica_Database\" TO your_user;"
```

## Support & Learning

- FastAPI Docs: https://fastapi.tiangolo.com/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- Pydantic Docs: https://docs.pydantic.dev/
- Alembic Docs: https://alembic.sqlalchemy.org/

## License

Private project for Chronica platform.

## Author

Built with ❤️ using FastAPI
