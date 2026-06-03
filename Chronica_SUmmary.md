# Chronica Backend — Full Project Summary

> **Generated:** 2026-06-03  
> **Author:** Project documentation auto-generated from full codebase analysis  
> **Purpose:** Complete reference for every file, module, class, function, endpoint, schema, and design decision in this project.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Dependencies](#3-dependencies)
4. [Environment Variables](#4-environment-variables)
5. [Complete File & Folder Structure](#5-complete-file--folder-structure)
6. [File-by-File Breakdown](#6-file-by-file-breakdown)
   - [Root Files](#61-root-files)
   - [app/main.py](#62-appmainpy)
   - [app/core/config.py](#63-appcoreconfigpy)
   - [app/core/security.py](#64-appcoresecuritypy)
   - [app/db/database.py](#65-appdbdatabasepy)
   - [app/models/models.py](#66-appmodelsmodelspy)
   - [app/schemas/auth.py](#67-appschemasauthpy)
   - [app/schemas/chess_game.py](#68-appschemaschester_gamepy)
   - [app/services/auth.py](#69-appservicesauthpy)
   - [app/services/chess_game.py](#610-appserviceschess_gamepy)
   - [app/api/v1/endpoints/auth.py](#611-appapiv1endpointsauthpy)
   - [app/api/v1/endpoints/chess_games.py](#612-appapiv1endpointschess_gamespy)
   - [app/utils/dependencies.py](#613-apputilsdependenciespy)
   - [Module Init Files](#614-module-init-files)
   - [Alembic Migration Files](#615-alembic-migration-files)
   - [Docker Files](#616-docker-files)
   - [Setup & Documentation Files](#617-setup--documentation-files)
7. [Database Models & Schema](#7-database-models--schema)
8. [Pydantic Validation Schemas](#8-pydantic-validation-schemas)
9. [API Endpoints Reference](#9-api-endpoints-reference)
10. [Authentication & Security](#10-authentication--security)
11. [Service Layer Logic](#11-service-layer-logic)
12. [Request Lifecycle / Data Flow](#12-request-lifecycle--data-flow)
13. [Database Migrations](#13-database-migrations)
14. [Docker & Deployment](#14-docker--deployment)
15. [Architecture Patterns & Conventions](#15-architecture-patterns--conventions)
16. [Project Statistics](#16-project-statistics)
17. [How to Run](#17-how-to-run)

---

## 1. Project Overview

| Field              | Value                                  |
| ------------------ | -------------------------------------- |
| **Project Name**   | Chronica Backend                       |
| **Type**           | REST API Backend                       |
| **Domain**         | Personal Knowledge Management Platform |
| **Framework**      | FastAPI (Python)                       |
| **Database**       | PostgreSQL                             |
| **ORM**            | SQLAlchemy 2.0                         |
| **Auth**           | JWT (JSON Web Tokens)                  |
| **API Version**    | v1                                     |
| **Status**         | Production-Ready                       |
| **Python Version** | 3.11+                                  |

**What it does:**  
Chronica Backend is the server-side API for the Chronica personal productivity platform. Currently it implements two domains:

1. **User Authentication** — registration, login, JWT session management
2. **Chess Games** — full CRUD for tracking chess game records, with statistics and filtering

The codebase is architecturally designed to be extensible. Future modules (diary, holiday calendar, notes, analytics) can be added by following the same layered pattern already established.

---

## 2. Technology Stack

| Layer            | Technology        | Version | Purpose                                     |
| ---------------- | ----------------- | ------- | ------------------------------------------- |
| Web Framework    | FastAPI           | 0.104.1 | HTTP routing, dependency injection, OpenAPI |
| ASGI Server      | Uvicorn           | 0.24.0  | Run the FastAPI app                         |
| ORM              | SQLAlchemy        | 2.0.23  | Database queries and model mapping          |
| Migrations       | Alembic           | 1.13.0  | Database schema versioning                  |
| DB Driver        | psycopg[binary]   | 3.3.4   | PostgreSQL connection adapter               |
| Validation       | Pydantic          | 2.5.0   | Request/response schema validation          |
| Settings         | pydantic-settings | 2.1.0   | Load config from .env file                  |
| Env Files        | python-dotenv     | 1.0.0   | .env file parsing                           |
| Auth Tokens      | python-jose       | 3.3.0   | JWT encode/decode with cryptography         |
| Passwords        | passlib[bcrypt]   | 1.7.4   | Bcrypt password hashing                     |
| Email            | email-validator   | 2.1.0   | Email address validation                    |
| Forms            | python-multipart  | 0.0.6   | Multipart form data support                 |
| Database         | PostgreSQL        | 15      | Relational data storage                     |
| Containerization | Docker            | —       | Build and run the application               |
| Orchestration    | Docker Compose    | —       | Multi-container development environment     |

---

## 3. Dependencies

**File:** `requirements.txt`

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.13.0
psycopg[binary]==3.3.4
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
email-validator==2.1.0
python-multipart==0.0.6
```

**Notable choices:**

- `psycopg[binary]` (v3) — Newer psycopg3 driver, not the older psycopg2
- `python-jose[cryptography]` — Cryptography extras required for HS256/RS256
- `passlib[bcrypt]` — bcrypt extras for strong password hashing
- `pydantic-settings` — Separate package in Pydantic v2 (was included in v1)

---

## 4. Environment Variables

**File:** `.env.example`  
**Loaded by:** `app/core/config.py` via pydantic-settings

| Variable                      | Default                                                           | Description                             |
| ----------------------------- | ----------------------------------------------------------------- | --------------------------------------- |
| `DATABASE_URL`                | `postgresql://username:password@localhost:5432/Chronica_Database` | PostgreSQL connection string            |
| `SECRET_KEY`                  | `your-secret-key-change-this-in-production`                       | JWT signing secret                      |
| `ALGORITHM`                   | `HS256`                                                           | JWT signing algorithm                   |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080`                                                           | Token lifetime (7 days = 10080 minutes) |
| `API_TITLE`                   | `Chronica API`                                                    | OpenAPI title                           |
| `API_VERSION`                 | `1.0.0`                                                           | OpenAPI version                         |
| `API_DESCRIPTION`             | `Personal Knowledge Management Platform Backend`                  | OpenAPI description                     |
| `ENVIRONMENT`                 | `development`                                                     | Environment name                        |
| `DEBUG`                       | `True`                                                            | Enables SQL query logging               |
| `BACKEND_CORS_ORIGINS`        | `["http://localhost:5173","http://localhost:3000"]`               | Allowed CORS origins                    |

> In production, always replace `SECRET_KEY` with a strong random value (e.g., `openssl rand -hex 32`).

---

## 5. Complete File & Folder Structure

```
Chronica-Backend/
│
├── .env.example                         # Environment variable template
├── .gitignore                           # Git ignore rules
├── README.md                            # Project intro and overview
├── requirements.txt                     # Python package dependencies
├── setup.bat                            # Windows automated setup script
├── setup.sh                             # macOS/Linux automated setup script
├── Dockerfile                           # Docker image build instructions
├── docker-compose.yml                   # Multi-container Docker configuration
│
├── 00_START_HERE.md                     # Entry point guide for new developers
├── QUICK_START.md                       # 5-minute quick start
├── SETUP_GUIDE.md                       # Detailed local setup instructions
├── API_DOCUMENTATION.md                 # Full API reference (manual)
├── ARCHITECTURE.md                      # Architecture and design principles
├── DEPLOYMENT_GUIDE.md                  # Production deployment guide
├── DOCKER_GUIDE.md                      # Docker-specific usage guide
├── FILES_CREATED.md                     # Describes purpose of generated files
│
├── alembic/
│   ├── alembic.ini                      # Alembic CLI configuration
│   ├── env.py                           # Alembic environment (connects to app DB)
│   ├── script.py.mako                   # Migration file template
│   └── versions/
│       └── 001_initial_schema.py        # Initial DB schema migration
│
└── app/
    ├── __init__.py                      # Package marker
    ├── main.py                          # FastAPI app factory, entry point
    │
    ├── api/
    │   ├── __init__.py                  # Exports api_v1_router
    │   └── v1/
    │       ├── __init__.py              # Creates /api/v1 prefixed router
    │       └── endpoints/
    │           ├── __init__.py          # Combines auth + chess_games routers
    │           ├── auth.py              # Auth endpoints: register, login, logout
    │           └── chess_games.py       # Chess game endpoints: CRUD + stats
    │
    ├── core/
    │   ├── __init__.py                  # Exports Settings, get_settings
    │   ├── config.py                    # Pydantic settings, env var loading
    │   └── security.py                  # JWT token + password hash utilities
    │
    ├── db/
    │   ├── __init__.py                  # Exports engine, SessionLocal, get_db
    │   └── database.py                  # DB engine, session factory, get_db dep
    │
    ├── models/
    │   ├── __init__.py                  # Exports Base, User, ChessGame, GameResult
    │   └── models.py                    # SQLAlchemy ORM models (User, ChessGame)
    │
    ├── schemas/
    │   ├── __init__.py                  # Exports all schema classes
    │   ├── auth.py                      # Pydantic schemas for auth endpoints
    │   └── chess_game.py                # Pydantic schemas for chess game endpoints
    │
    ├── services/
    │   ├── __init__.py                  # Exports AuthService, ChessGameService
    │   ├── auth.py                      # Auth business logic (register, login)
    │   └── chess_game.py                # Chess game business logic (CRUD, stats)
    │
    └── utils/
        ├── __init__.py                  # Exports get_current_user
        └── dependencies.py              # FastAPI dependency: get_current_user
```

---

## 6. File-by-File Breakdown

### 6.1 Root Files

---

#### `.env.example`

Template for the `.env` configuration file. Contains all required environment variables with placeholder values. Developers copy this to `.env` and fill in real values. Never committed with real secrets.

---

#### `.gitignore`

Standard Python gitignore. Excludes: `__pycache__`, `*.pyc`, `.env`, virtual environment directories, IDE configs.

---

#### `requirements.txt`

Lists all Python package dependencies with pinned versions. Used by `pip install -r requirements.txt` during setup and Docker builds.

---

#### `setup.bat` / `setup.sh`

Automated setup scripts for Windows (`setup.bat`) and Unix/macOS (`setup.sh`). They create a virtual environment, install dependencies, copy `.env.example` to `.env`, and run Alembic migrations. Intended for first-time setup.

---

#### `Dockerfile`

Multi-step Docker image build for the API server. Details covered in [Section 14](#14-docker--deployment).

---

#### `docker-compose.yml`

Orchestrates three services: `postgres`, `api`, and `adminer`. Details covered in [Section 14](#14-docker--deployment).

---

#### Documentation files (`.md`)

Eight markdown documentation files are included:

| File                   | Purpose                                              |
| ---------------------- | ---------------------------------------------------- |
| `00_START_HERE.md`     | Entry point — where new developers should start      |
| `README.md`            | Project overview, tech stack, quick links            |
| `QUICK_START.md`       | Minimal steps to get running in under 5 minutes      |
| `SETUP_GUIDE.md`       | Full local setup with troubleshooting                |
| `API_DOCUMENTATION.md` | Hand-written full API reference                      |
| `ARCHITECTURE.md`      | Layered architecture explanation, design patterns    |
| `DEPLOYMENT_GUIDE.md`  | Production deployment to cloud (Neon, Railway, etc.) |
| `DOCKER_GUIDE.md`      | Docker Compose usage, volume management, Adminer     |

---

### 6.2 `app/main.py`

**Location:** `app/main.py`  
**Lines:** ~90  
**Purpose:** Application entry point and factory. Wires together all components.

**What it contains:**

| Element                            | Type              | Description                                                  |
| ---------------------------------- | ----------------- | ------------------------------------------------------------ |
| `create_app()`                     | Function          | Factory that creates and configures the FastAPI app instance |
| `app`                              | FastAPI instance  | The global ASGI app exposed to uvicorn                       |
| CORS middleware                    | Middleware        | Allows requests from whitelisted origins                     |
| Route registration                 | —                 | Includes `api_v1_router` with all API routes                 |
| `GET /health`                      | Endpoint          | Health check returning `{"status":"healthy"}`                |
| `validation_exception_handler`     | Exception handler | Custom JSON for Pydantic validation errors                   |
| `Base.metadata.create_all(engine)` | Startup           | Creates all DB tables if they don't exist                    |
| `uvicorn.run()` block              | Entry             | Runs the server when executed as `python -m app.main`        |

**CORS configuration:**

```
allow_origins  = settings.BACKEND_CORS_ORIGINS
allow_methods  = ["*"]
allow_headers  = ["*"]
allow_credentials = True
```

**Health check response:**

```json
{
  "status": "healthy",
  "environment": "development",
  "api_version": "1.0.0"
}
```

**OpenAPI docs are available at:**

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- OpenAPI JSON: `http://localhost:8000/api/openapi.json`

---

### 6.3 `app/core/config.py`

**Location:** `app/core/config.py`  
**Lines:** ~55  
**Purpose:** Centralized configuration using Pydantic Settings. Reads from environment variables and `.env` file.

**What it contains:**

| Element          | Type                 | Description                                                                       |
| ---------------- | -------------------- | --------------------------------------------------------------------------------- |
| `Settings`       | Class (BaseSettings) | All configuration variables with defaults and types                               |
| `get_settings()` | Function             | `@lru_cache()` singleton getter — returns the same `Settings` instance every call |
| `settings`       | Instance             | Module-level singleton used by other modules                                      |

**Settings class fields:**

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    API_TITLE: str = "Chronica API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "..."
    API_V1_PREFIX: str = "/api/v1"

    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    BACKEND_CORS_ORIGINS: List[str] = [...]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
```

The `@lru_cache()` on `get_settings()` ensures the `.env` file is parsed only once and the settings object is reused throughout the app lifetime.

---

### 6.4 `app/core/security.py`

**Location:** `app/core/security.py`  
**Lines:** ~115  
**Purpose:** All cryptographic operations — password hashing and JWT token management.

**What it contains:**

| Element         | Type         | Description                                               |
| --------------- | ------------ | --------------------------------------------------------- |
| `SecurityUtils` | Class        | Static utility class grouping all security operations     |
| `pwd_context`   | CryptContext | Passlib context configured for bcrypt with cost factor 12 |

**Methods on `SecurityUtils`:**

```python
@staticmethod
def hash_password(password: str) -> str
```

- Hashes a plain-text password using bcrypt
- Cost factor: 12 (computationally expensive, resists brute-force)
- Returns: 60-character bcrypt hash string
- Used in: `AuthService.register()`

```python
@staticmethod
def verify_password(plain_password: str, hashed_password: str) -> bool
```

- Compares a plain password against a stored bcrypt hash
- Uses constant-time comparison (prevents timing attacks)
- Returns: `True` if match, `False` otherwise
- Used in: `AuthService.login()`

```python
@staticmethod
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str
```

- Creates a signed JWT token
- Encodes payload: `{"sub": user_id, "exp": expiration_timestamp}`
- Algorithm: HS256 (HMAC-SHA256)
- Default expiry: `ACCESS_TOKEN_EXPIRE_MINUTES` (7 days)
- Returns: Encoded JWT string
- Used in: `AuthService._create_token()`

```python
@staticmethod
def decode_token(token: str) -> Dict[str, Any]
```

- Decodes and validates a JWT token
- Validates: Signature integrity, expiration time, token format
- Returns: Decoded payload dict with `"sub"` (user_id)
- Raises: `HTTPException(401)` if token is invalid or expired
- Used in: `get_current_user()` dependency

---

### 6.5 `app/db/database.py`

**Location:** `app/db/database.py`  
**Lines:** ~44  
**Purpose:** Database engine setup, session factory, and the `get_db` dependency.

**What it contains:**

| Element        | Type               | Description                                                     |
| -------------- | ------------------ | --------------------------------------------------------------- |
| `engine`       | SQLAlchemy Engine  | Database connection pool connected to `DATABASE_URL`            |
| `SessionLocal` | sessionmaker       | Session factory used to create per-request DB sessions          |
| `get_db()`     | Generator function | FastAPI dependency that yields a DB session and ensures cleanup |

**Engine configuration:**

```python
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,   # Logs all SQL queries when DEBUG=True
    future=True,           # Use SQLAlchemy 2.0 style
)
```

**Session factory:**

```python
SessionLocal = sessionmaker(
    autocommit=False,       # Transactions must be committed explicitly
    autoflush=False,        # Don't auto-flush before queries
    bind=engine,
    expire_on_commit=False, # Keep objects accessible after commit
)
```

**`get_db()` dependency:**

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db        # Provide session to endpoint handler
    finally:
        db.close()      # Always close session, even on error
```

This is injected into endpoint handlers using `Depends(get_db)`.

---

### 6.6 `app/models/models.py`

**Location:** `app/models/models.py`  
**Lines:** ~69  
**Purpose:** SQLAlchemy ORM model definitions for all database tables.

**What it contains:**

| Element      | Type            | Description                                   |
| ------------ | --------------- | --------------------------------------------- |
| `Base`       | DeclarativeBase | SQLAlchemy base class all models inherit from |
| `GameResult` | Enum class      | `win`, `loss`, `draw` values for game results |
| `User`       | Model class     | Maps to the `users` PostgreSQL table          |
| `ChessGame`  | Model class     | Maps to the `chess_games` PostgreSQL table    |

#### `User` Model

```python
class User(Base):
    __tablename__ = "users"

    id           : String(36)   — UUID primary key
    name         : String(80)   — User's full name, indexed, not nullable
    email        : String(255)  — Unique email, indexed, not nullable
    password_hash: String(255)  — bcrypt hash, not nullable
    created_at   : DateTime     — Account creation time, default=now()
    updated_at   : DateTime     — Last update time, default=now(), onupdate=now()

    Relationships:
    chess_games  — One-to-many → ChessGame (cascade="all, delete-orphan")
```

**Indexes on `users`:** `email` (UNIQUE), `name`

#### `ChessGame` Model

```python
class ChessGame(Base):
    __tablename__ = "chess_games"

    id        : String(36)    — UUID primary key
    user_id   : String(36)    — FK to users.id, CASCADE DELETE, indexed
    title     : String(120)   — Game title, indexed, not nullable
    opponent  : String(100)   — Opponent name, not nullable
    result    : GameResult    — Enum: win/loss/draw, indexed
    opening   : String(120)   — Chess opening name, nullable, default ""
    notes     : Text          — Game notes/analysis, nullable, default ""
    created_at: DateTime      — Creation timestamp, indexed, default=now()
    updated_at: DateTime      — Last update, default=now(), onupdate=now()

    Relationships:
    user      — Many-to-one → User
```

**Indexes on `chess_games`:** `user_id`, `title`, `result`, `created_at`

#### `GameResult` Enum

```python
class GameResult(str, enum.Enum):
    WIN  = "win"
    LOSS = "loss"
    DRAW = "draw"
```

Inherits from `str` so it serializes directly to/from JSON strings.

---

### 6.7 `app/schemas/auth.py`

**Location:** `app/schemas/auth.py`  
**Lines:** ~55  
**Purpose:** Pydantic v2 models for validating auth endpoint request bodies and shaping response data.

**Classes:**

#### `UserBase`

```python
name  : str  (1–80 characters)
email : EmailStr
```

Base class with common user fields.

#### `UserCreate` (extends `UserBase`)

```python
password : str  (8–100 characters)
```

Used for `POST /auth/register` request body validation. Adds password requirement.

#### `UserResponse` (extends `UserBase`)

```python
id         : str
created_at : datetime
```

Used as the user object in API responses. Does NOT include password. `model_config = ConfigDict(from_attributes=True)` enables ORM-to-schema conversion.

#### `LoginRequest`

```python
email    : EmailStr
password : str
```

Used for `POST /auth/login` request body. Minimal login credentials.

#### `AuthSessionResponse`

```python
user       : UserResponse
token      : str        — JWT bearer token
expires_at : datetime   — Token expiration timestamp
```

Returned by both `register` and `login` endpoints. One unified response for session creation.

#### `TokenData`

```python
user_id : Optional[str] = None
```

Internal schema representing the decoded JWT payload used in `get_current_user()`.

---

### 6.8 `app/schemas/chess_game.py`

**Location:** `app/schemas/chess_game.py`  
**Lines:** ~111  
**Purpose:** Pydantic v2 models for chess game request/response validation.

**Classes:**

#### `GameResultEnum` (Python Enum)

```python
WIN  = "win"
LOSS = "loss"
DRAW = "draw"
```

Schema-level enum (separate from the SQLAlchemy model-level `GameResult` enum).

#### `ChessGameBase`

```python
title    : str   (1–120 chars, required)
opponent : str   (1–100 chars, required)
result   : GameResultEnum (required)
opening  : str   (0–120 chars, optional, default "")
notes    : str   (0–8000 chars, optional, default "")
```

Base schema with all chess game content fields.

#### `ChessGameCreate` (extends `ChessGameBase`)

No additional fields. Used as request body for `POST /chess-games`.

#### `ChessGameUpdate`

All fields optional for partial (PATCH) updates:

```python
title    : Optional[str]           (1–120 chars)
opponent : Optional[str]           (1–100 chars)
result   : Optional[GameResultEnum]
opening  : Optional[str]           (0–120 chars)
notes    : Optional[str]           (0–8000 chars)
```

#### `ChessGameResponse` (extends `ChessGameBase`)

```python
id         : str
user_id    : str
created_at : datetime
updated_at : datetime
```

Returned by all endpoints that return a single game. Includes all base fields plus metadata. `from_attributes=True` for ORM conversion.

#### `ChessGameListResponse`

```python
data  : List[ChessGameResponse]
total : int
```

Wrapper for list endpoints. Includes the count alongside the data array.

#### `ChessGameStatsResponse`

```python
total    : int
wins     : int
losses   : int
draws    : int
win_rate : float   (0.0 – 100.0, percentage)
```

Returned by `GET /chess-games/stats`.

---

### 6.9 `app/services/auth.py`

**Location:** `app/services/auth.py`  
**Lines:** ~171  
**Purpose:** All authentication business logic — registration, login, token creation.

**Class: `AuthService`**

Constructor:

```python
def __init__(self, db: Session):
    self.db = db
    self.security = SecurityUtils()
```

**Methods:**

```python
def register(self, user_data: UserCreate) -> AuthSessionResponse
```

1. Queries DB to check if email already exists → `400` if so
2. Hashes password with bcrypt
3. Creates `User` object with UUID, name, email, password_hash
4. Commits to DB
5. Calls `_create_token(user.id)` to get JWT + expiration
6. Returns `AuthSessionResponse(user, token, expires_at)`
7. On DB error: rolls back and raises `500`

```python
def login(self, login_data: LoginRequest) -> AuthSessionResponse
```

1. Queries DB for user by email → `401` if not found
2. Verifies plain password against stored hash → `401` if mismatch
3. Calls `_create_token(user.id)`
4. Returns `AuthSessionResponse(user, token, expires_at)`

```python
def get_user_by_id(self, user_id: str) -> User
```

1. Queries DB for user by primary key `id`
2. Returns `User` object or raises `404`

```python
@staticmethod
def _create_token(user_id: str) -> Tuple[str, datetime]
```

1. Computes `expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)`
2. Calls `SecurityUtils.create_access_token({"sub": user_id})`
3. Returns `(token_string, expires_at_datetime)`

---

### 6.10 `app/services/chess_game.py`

**Location:** `app/services/chess_game.py`  
**Lines:** ~241  
**Purpose:** All chess game business logic — CRUD operations, statistics, recent games.

**Class: `ChessGameService`**

Constructor:

```python
def __init__(self, db: Session):
    self.db = db
```

**Methods:**

```python
def create_game(self, user_id: str, game_data: ChessGameCreate) -> ChessGameResponse
```

1. Verifies user exists (calls `_get_user_or_404`)
2. Creates `ChessGame` object with UUID and all provided fields
3. Commits to DB
4. Returns `ChessGameResponse`

```python
def get_all_games(self, user_id: str) -> List[ChessGameResponse]
```

1. Verifies user exists
2. Queries all `ChessGame` where `user_id` matches
3. Orders by `created_at DESC` (newest first)
4. Returns list of `ChessGameResponse`

```python
def get_game_by_id(self, user_id: str, game_id: str) -> ChessGameResponse
```

1. Queries `ChessGame` by `id=game_id AND user_id=user_id`
2. Returns `ChessGameResponse` or `404` if not found/not owned by user

```python
def update_game(self, user_id: str, game_id: str, game_data: ChessGameUpdate) -> ChessGameResponse
```

1. Fetches game (user-owned)
2. For each field in `game_data`, if not `None`, updates the model field
3. Sets `updated_at = datetime.utcnow()`
4. Commits to DB
5. Returns updated `ChessGameResponse`

```python
def delete_game(self, user_id: str, game_id: str) -> None
```

1. Fetches game (user-owned) or `404`
2. Deletes from DB and commits

```python
def get_game_stats(self, user_id: str) -> ChessGameStatsResponse
```

1. Queries all games for user
2. Counts total, wins, losses, draws using Python list operations
3. Calculates `win_rate = (wins / total) * 100` if total > 0, else 0.0
4. Returns `ChessGameStatsResponse`

```python
def get_recent_games(self, user_id: str, limit: int = 5) -> List[ChessGameResponse]
```

1. Queries user's games ordered by `created_at DESC`
2. Limits to `limit` results
3. Returns list of `ChessGameResponse`

**Private helper:**

```python
def _get_user_or_404(self, user_id: str) -> User
```

Queries for user; raises `404` if not found. Used internally by other methods.

---

### 6.11 `app/api/v1/endpoints/auth.py`

**Location:** `app/api/v1/endpoints/auth.py`  
**Lines:** ~71  
**Purpose:** FastAPI route handlers for authentication. Thin layer — delegates all logic to `AuthService`.

**Router:** `APIRouter(prefix="/auth", tags=["Authentication"])`

**Endpoints defined here:**

| Route            | Method | Status | Handler Function  |
| ---------------- | ------ | ------ | ----------------- |
| `/auth/register` | POST   | 201    | `register_user()` |
| `/auth/login`    | POST   | 200    | `login_user()`    |
| `/auth/logout`   | POST   | 200    | `logout_user()`   |

**`register_user()`**

- Accepts: `UserCreate` request body
- Creates: `AuthService(db)`, calls `.register(user_data)`
- Returns: `AuthSessionResponse`

**`login_user()`**

- Accepts: `LoginRequest` request body
- Creates: `AuthService(db)`, calls `.login(login_data)`
- Returns: `AuthSessionResponse`

**`logout_user()`**

- No request body required
- No token validation (JWT is stateless; logout is client-side)
- Returns: `{"message": "Logged out successfully"}`

---

### 6.12 `app/api/v1/endpoints/chess_games.py`

**Location:** `app/api/v1/endpoints/chess_games.py`  
**Lines:** ~177  
**Purpose:** FastAPI route handlers for chess game CRUD, statistics, and recent listing. All routes require authentication.

**Router:** `APIRouter(prefix="/chess-games", tags=["Chess Games"])`

**Endpoints defined here:**

| Route                    | Method | Status | Handler Function     |
| ------------------------ | ------ | ------ | -------------------- |
| `/chess-games`           | GET    | 200    | `get_all_games()`    |
| `/chess-games`           | POST   | 201    | `create_game()`      |
| `/chess-games/stats`     | GET    | 200    | `get_game_stats()`   |
| `/chess-games/recent`    | GET    | 200    | `get_recent_games()` |
| `/chess-games/{game_id}` | GET    | 200    | `get_game()`         |
| `/chess-games/{game_id}` | PATCH  | 200    | `update_game()`      |
| `/chess-games/{game_id}` | DELETE | 204    | `delete_game()`      |

All handlers follow the same pattern:

1. Receive `current_user: User = Depends(get_current_user)` and `db: Session = Depends(get_db)`
2. Instantiate `ChessGameService(db)`
3. Call the appropriate service method with `current_user.id`
4. Return the result

> **Important routing order note:** `/stats` and `/recent` are registered **before** `/{game_id}` to prevent FastAPI from matching them as `game_id` path parameters.

---

### 6.13 `app/utils/dependencies.py`

**Location:** `app/utils/dependencies.py`  
**Lines:** ~65  
**Purpose:** FastAPI dependency functions. Currently contains the JWT authentication dependency.

**Dependencies:**

```python
security = HTTPBearer()
```

FastAPI security scheme that extracts the Bearer token from the `Authorization` header.

```python
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
```

**Process:**

1. FastAPI extracts `Authorization: Bearer <token>` via `HTTPBearer()`
2. `SecurityUtils.decode_token(credentials.credentials)` decodes and validates the JWT
3. Extracts `user_id` from the token's `"sub"` claim
4. Queries the database for a `User` with that ID
5. Returns the `User` object if found
6. Raises `HTTPException(401, "Could not validate credentials")` if:
   - Token is invalid or expired
   - User ID not in token
   - User not found in DB

**Usage in endpoints:**

```python
current_user: User = Depends(get_current_user)
```

---

### 6.14 Module Init Files

| File                               | What it exports                                                                                                                                                                                                    |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `app/__init__.py`                  | Empty (package marker)                                                                                                                                                                                             |
| `app/api/__init__.py`              | `api_v1_router` from `app.api.v1`                                                                                                                                                                                  |
| `app/api/v1/__init__.py`           | `router` — APIRouter with prefix `/api/v1` including all endpoint routers                                                                                                                                          |
| `app/api/v1/endpoints/__init__.py` | `api_router` — Combined router with auth and chess_games routers                                                                                                                                                   |
| `app/core/__init__.py`             | `Settings`, `get_settings`                                                                                                                                                                                         |
| `app/db/__init__.py`               | `engine`, `SessionLocal`, `get_db`                                                                                                                                                                                 |
| `app/models/__init__.py`           | `Base`, `User`, `ChessGame`, `GameResult`                                                                                                                                                                          |
| `app/schemas/__init__.py`          | All schema classes: `UserCreate`, `UserResponse`, `LoginRequest`, `AuthSessionResponse`, `TokenData`, `ChessGameCreate`, `ChessGameUpdate`, `ChessGameResponse`, `ChessGameListResponse`, `ChessGameStatsResponse` |
| `app/services/__init__.py`         | `AuthService`, `ChessGameService`                                                                                                                                                                                  |
| `app/utils/__init__.py`            | `get_current_user`                                                                                                                                                                                                 |

---

### 6.15 Alembic Migration Files

#### `alembic/alembic.ini`

Alembic CLI configuration. Sets `script_location = alembic`, `sqlalchemy.url` is overridden in `env.py` to use the app's `DATABASE_URL`.

#### `alembic/env.py`

Alembic environment file that:

- Imports app's `Base` and all models (so Alembic can detect schema)
- Imports `settings` to get `DATABASE_URL`
- Configures both offline (SQL script) and online (live DB) migration modes

#### `alembic/script.py.mako`

Template used to generate new migration files. Includes standard imports and the `upgrade()`/`downgrade()` function stubs.

#### `alembic/versions/001_initial_schema.py`

**Revision:** `001`  
**Message:** `initial_schema`

**`upgrade()` function creates:**

1. `GameResult` PostgreSQL enum type: `('win', 'loss', 'draw')`
2. `users` table with columns and constraints
3. Indexes: `ix_users_email` (UNIQUE), `ix_users_name`
4. `chess_games` table with columns and constraints
5. `ForeignKeyConstraint`: `chess_games.user_id → users.id` with `ondelete="CASCADE"`
6. Indexes: `ix_chess_games_user_id`, `ix_chess_games_title`, `ix_chess_games_result`, `ix_chess_games_created_at`

**`downgrade()` function drops:**

1. Indexes on `chess_games`
2. `chess_games` table
3. Indexes on `users`
4. `users` table
5. `GameResult` enum type

---

### 6.16 Docker Files

#### `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install OS dependencies: gcc (for compiling psycopg), postgresql-client
RUN apt-get update && apt-get install -y gcc postgresql-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Health check polls /health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### `docker-compose.yml`

Three services:

**1. `postgres`**

- Image: `postgres:15-alpine`
- Port: `5432:5432`
- Environment: `POSTGRES_DB=Chronica_Database`, `POSTGRES_USER=chronica_user`, `POSTGRES_PASSWORD=chronica_password`
- Volume: `postgres_data` (persistent)
- Healthcheck: `pg_isready`

**2. `api`**

- Build context: current directory using `Dockerfile`
- Port: `8000:8000`
- Depends on: `postgres` (waits for healthcheck to pass)
- Environment: All settings from `DATABASE_URL` through `BACKEND_CORS_ORIGINS`
- Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

**3. `adminer`**

- Image: `adminer` (lightweight DB GUI)
- Port: `8080:8080`
- Access: `http://localhost:8080` — visual PostgreSQL management interface

**Network:** `chronica_network` (bridge driver, all services connected)

---

### 6.17 Setup & Documentation Files

#### `setup.bat` (Windows)

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
echo Setup complete!
```

#### `setup.sh` (Unix/macOS)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
echo "Setup complete!"
```

---

## 7. Database Models & Schema

### Entity-Relationship Diagram

```
┌─────────────────────────────────┐
│            users                │
├─────────────────────────────────┤
│ id (PK, UUID String)            │
│ name (String 80, indexed)       │
│ email (String 255, UNIQUE)      │
│ password_hash (String 255)      │
│ created_at (DateTime)           │
│ updated_at (DateTime)           │
└────────────────┬────────────────┘
                 │ 1
                 │ (cascade delete)
                 │ N
┌────────────────▼────────────────┐
│          chess_games             │
├─────────────────────────────────┤
│ id (PK, UUID String)            │
│ user_id (FK → users.id)         │
│ title (String 120, indexed)     │
│ opponent (String 100)           │
│ result (Enum: win/loss/draw)    │
│ opening (String 120, nullable)  │
│ notes (Text, nullable)          │
│ created_at (DateTime, indexed)  │
│ updated_at (DateTime)           │
└─────────────────────────────────┘
```

### All Database Indexes

| Table       | Index Name                  | Columns    | Type    |
| ----------- | --------------------------- | ---------- | ------- |
| users       | `ix_users_email`            | email      | UNIQUE  |
| users       | `ix_users_name`             | name       | Regular |
| chess_games | `ix_chess_games_user_id`    | user_id    | Regular |
| chess_games | `ix_chess_games_title`      | title      | Regular |
| chess_games | `ix_chess_games_result`     | result     | Regular |
| chess_games | `ix_chess_games_created_at` | created_at | Regular |

---

## 8. Pydantic Validation Schemas

### Auth Schemas (`app/schemas/auth.py`)

```
UserBase
├── UserCreate  (adds: password min 8 chars)
└── UserResponse (adds: id, created_at — no password)

LoginRequest         (email + password)
AuthSessionResponse  (user: UserResponse + token + expires_at)
TokenData            (user_id: Optional[str])
```

### Chess Game Schemas (`app/schemas/chess_game.py`)

```
ChessGameBase  (title, opponent, result, opening, notes)
├── ChessGameCreate  (no additions — direct use for POST)
└── ChessGameResponse  (adds: id, user_id, created_at, updated_at)

ChessGameUpdate      (all fields Optional — for PATCH)
ChessGameListResponse  (data: List[ChessGameResponse], total: int)
ChessGameStatsResponse  (total, wins, losses, draws, win_rate)
```

### Field Validation Summary

| Field                 | Min Length | Max Length | Validation                  |
| --------------------- | ---------- | ---------- | --------------------------- |
| `name`                | 1          | 80         | —                           |
| `email`               | —          | —          | Valid email format          |
| `password`            | 8          | 100        | —                           |
| `title`               | 1          | 120        | —                           |
| `opponent`            | 1          | 100        | —                           |
| `result`              | —          | —          | Must be `win`/`loss`/`draw` |
| `opening`             | 0          | 120        | —                           |
| `notes`               | 0          | 8000       | —                           |
| `limit` (query param) | 1          | 50         | Integer range               |

---

## 9. API Endpoints Reference

**Base URL:** `http://localhost:8000`  
**API prefix:** `/api/v1`

### Complete Endpoint Table

| #   | Method | Path                                 | Auth Required | Success Code | Description             |
| --- | ------ | ------------------------------------ | ------------- | ------------ | ----------------------- |
| 1   | GET    | `/health`                            | No            | 200          | Health check            |
| 2   | POST   | `/api/v1/auth/register`              | No            | 201          | Register new user       |
| 3   | POST   | `/api/v1/auth/login`                 | No            | 200          | Login and get JWT       |
| 4   | POST   | `/api/v1/auth/logout`                | No            | 200          | Logout (client cleanup) |
| 5   | GET    | `/api/v1/chess-games`                | Yes           | 200          | List all user's games   |
| 6   | POST   | `/api/v1/chess-games`                | Yes           | 201          | Create new game record  |
| 7   | GET    | `/api/v1/chess-games/stats`          | Yes           | 200          | Get win/loss/draw stats |
| 8   | GET    | `/api/v1/chess-games/recent?limit=N` | Yes           | 200          | Get N most recent games |
| 9   | GET    | `/api/v1/chess-games/{game_id}`      | Yes           | 200          | Get single game by ID   |
| 10  | PATCH  | `/api/v1/chess-games/{game_id}`      | Yes           | 200          | Partial update a game   |
| 11  | DELETE | `/api/v1/chess-games/{game_id}`      | Yes           | 204          | Delete a game           |

**Total: 11 endpoints**

### Request/Response Detail

#### `POST /api/v1/auth/register`

**Request:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response (201):**

```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2026-06-03T10:30:00"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2026-06-10T10:30:00"
}
```

#### `POST /api/v1/auth/login`

**Request:**

```json
{ "email": "john@example.com", "password": "securepassword" }
```

**Response (200):** Same shape as register response.

#### `GET /api/v1/chess-games`

**Headers:** `Authorization: Bearer <token>`  
**Response (200):**

```json
[
  {
    "id": "660e8400-...",
    "user_id": "550e8400-...",
    "title": "Tournament Round 3",
    "opponent": "Magnus Carlsen",
    "result": "win",
    "opening": "Sicilian Defense",
    "notes": "Played well in the endgame",
    "created_at": "2026-06-03T10:35:00",
    "updated_at": "2026-06-03T10:35:00"
  }
]
```

#### `POST /api/v1/chess-games`

**Request:**

```json
{
  "title": "Club Match",
  "opponent": "Alice Smith",
  "result": "draw",
  "opening": "King's Indian",
  "notes": "Tough endgame"
}
```

**Response (201):** Full `ChessGameResponse` with generated `id`, `user_id`, timestamps.

#### `GET /api/v1/chess-games/stats`

**Response (200):**

```json
{ "total": 15, "wins": 10, "losses": 3, "draws": 2, "win_rate": 66.67 }
```

#### `GET /api/v1/chess-games/recent?limit=3`

**Response (200):** Array of up to 3 `ChessGameResponse` objects, newest first.

#### `PATCH /api/v1/chess-games/{game_id}`

**Request (only include fields to change):**

```json
{ "result": "loss", "notes": "Blundered in time pressure" }
```

**Response (200):** Updated `ChessGameResponse`.

#### `DELETE /api/v1/chess-games/{game_id}`

**Response:** `204 No Content` (empty body)

### Error Response Formats

**400 Bad Request (e.g., email exists):**

```json
{ "detail": "Email already registered" }
```

**401 Unauthorized:**

```json
{ "detail": "Could not validate credentials" }
```

**404 Not Found:**

```json
{ "detail": "Chess game not found" }
```

**422 Unprocessable Entity (validation error):**

```json
{
  "detail": "Validation error",
  "errors": [
    {
      "loc": ["body", "password"],
      "msg": "String should have at least 8 characters",
      "type": "string_too_short"
    }
  ]
}
```

---

## 10. Authentication & Security

### JWT Token Structure

**Header:**

```json
{ "alg": "HS256", "typ": "JWT" }
```

**Payload:**

```json
{
  "sub": "user-uuid-here",
  "exp": 1749891600
}
```

**Signature:** HMAC-SHA256 of `base64(header).base64(payload)` with `SECRET_KEY`

### Authentication Flow

```
Registration:
  Client → POST /register (name, email, password)
        ← Check email uniqueness
        ← Hash password (bcrypt, cost=12)
        ← Insert user to DB
        ← Create JWT token (exp: +7 days)
  Client ← 201: {user, token, expires_at}

Login:
  Client → POST /login (email, password)
        ← Look up user by email
        ← Verify password hash
        ← Create JWT token
  Client ← 200: {user, token, expires_at}

Protected Request:
  Client → GET /chess-games
           Authorization: Bearer eyJ...
        ← HTTPBearer extracts token
        ← jose.decode(token, SECRET_KEY, algorithms=["HS256"])
        ← Extract sub (user_id)
        ← Query DB for user
  Client ← 200: [...games]
```

### Password Security Details

- **Algorithm:** bcrypt
- **Cost factor:** 12 (each check takes ~300ms, resistant to GPU brute-force)
- **Storage:** Only the hash is stored, never the plaintext

### User Data Isolation

Every service method that accesses user data filters by both the resource ID **and** the authenticated user's ID:

```python
db.query(ChessGame).filter(
    ChessGame.id == game_id,
    ChessGame.user_id == user_id  # Prevents accessing other users' data
).first()
```

This means a user cannot read, update, or delete another user's records even with a valid token.

---

## 11. Service Layer Logic

### Separation of Concerns

```
┌──────────────────────────────────────────────────────┐
│ Endpoint Handler (app/api/)                          │
│  - Route definition                                  │
│  - Dependency injection                              │
│  - Thin delegation to service                        │
└──────────────────┬───────────────────────────────────┘
                   │ calls
┌──────────────────▼───────────────────────────────────┐
│ Service Layer (app/services/)                        │
│  - Business logic                                    │
│  - Authorization checks                              │
│  - Database queries                                  │
│  - Error raising                                     │
└──────────────────┬───────────────────────────────────┘
                   │ uses
┌──────────────────▼───────────────────────────────────┐
│ ORM Models (app/models/)                             │
│  - Database table definitions                        │
│  - Relationships                                     │
└──────────────────────────────────────────────────────┘
```

### Service Instantiation Pattern

Services are instantiated **per request**, not as singletons, because each request gets its own database session:

```python
@router.get("/chess-games")
async def get_all_games(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ChessGameService(db)          # New instance per request
    return service.get_all_games(current_user.id)
```

---

## 12. Request Lifecycle / Data Flow

```
HTTP Request
    │
    ▼
FastAPI Router
(matches method + path)
    │
    ▼
Middleware
(CORS validation, header processing)
    │
    ▼
Dependency Resolution
├── Depends(get_current_user)
│   ├── HTTPBearer extracts Authorization header
│   ├── SecurityUtils.decode_token() validates JWT
│   ├── DB query for User by user_id
│   └── Returns User object  ──→  401 if invalid
│
├── Depends(get_db)
│   └── Creates Session, yields it
│
└── Pydantic schema validation
    └── Validates JSON request body  ──→  422 if invalid
    │
    ▼
Endpoint Handler Function
├── Receives: validated_body, current_user, db
├── Creates Service(db)
├── Calls service.method(current_user.id, ...)
└── Returns result
    │
    ▼
Service Method
├── Business logic
├── DB queries via SQLAlchemy ORM
├── Raises HTTPException if errors
└── Returns Pydantic schema or raises exception
    │
    ▼
Response Serialization
(Pydantic serializes ORM model → JSON)
    │
    ▼
HTTP Response
(JSON body, status code, headers)
```

---

## 13. Database Migrations

**Tool:** Alembic  
**Migration directory:** `alembic/versions/`

### Running Migrations

```bash
# Apply all migrations (create tables)
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback all migrations (drop all tables)
alembic downgrade base

# Check current migration version
alembic current

# View migration history
alembic history

# Create a new migration (auto-detect changes)
alembic revision --autogenerate -m "description"
```

### Migration `001_initial_schema.py`

Creates the complete initial database schema:

1. `GameResult` PostgreSQL enum type
2. `users` table + indexes
3. `chess_games` table + foreign key + indexes

The `downgrade()` function cleanly reverses all of this in reverse order, enabling safe rollback.

---

## 14. Docker & Deployment

### Development with Docker Compose

```bash
# Start all services (postgres + api + adminer)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop all services
docker-compose down

# Stop and remove volumes (wipes database)
docker-compose down -v

# Rebuild after code changes
docker-compose up -d --build
```

**Ports after startup:**
| Service | URL |
|---|---|
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/api/docs |
| Adminer (DB GUI) | http://localhost:8080 |
| PostgreSQL | localhost:5432 |

### Production Deployment Notes

For production (`DEPLOYMENT_GUIDE.md`):

- Set `ENVIRONMENT=production`, `DEBUG=False`
- Use a strong random `SECRET_KEY` (e.g., 64 hex chars from `openssl rand -hex 32`)
- Use a managed PostgreSQL (Neon, Supabase, AWS RDS, etc.)
- Restrict `BACKEND_CORS_ORIGINS` to only the production frontend URL
- Run behind a reverse proxy (Nginx, Caddy) for SSL termination
- Do not use `--reload` flag in production uvicorn command

---

## 15. Architecture Patterns & Conventions

### Layered Architecture

```
Presentation  │ app/api/v1/endpoints/     — HTTP routes, thin handlers
Business      │ app/services/             — Business logic, validation, auth
Data Access   │ app/models/               — ORM models
Infrastructure│ app/db/, app/core/        — DB connections, config, security
Contracts     │ app/schemas/              — Pydantic I/O contracts
Utilities     │ app/utils/                — Shared dependencies
```

### Key Patterns Used

**1. Dependency Injection (FastAPI `Depends`)**
Every endpoint receives its database session and current user via DI. No global state.

**2. Repository-less Service Pattern**
Services directly use the SQLAlchemy session for queries. The service layer IS the repository layer for this project's scale.

**3. Partial Update (PATCH) Pattern**
Only `ChessGameUpdate` fields that are not `None` are applied:

```python
update_data = game_data.model_dump(exclude_unset=True)
for field, value in update_data.items():
    setattr(game, field, value)
```

**4. UUID Primary Keys**
All primary keys are UUID strings generated at creation time (`str(uuid.uuid4())`), preventing sequential ID enumeration.

**5. Cascading Deletes**
Deleting a `User` automatically deletes all their `ChessGame` records via SQLAlchemy `cascade="all, delete-orphan"` and a database-level `ON DELETE CASCADE` foreign key.

**6. Singleton Settings**
`get_settings()` uses `@lru_cache()` so the `.env` file is parsed exactly once.

**7. Non-root Docker User**
The Docker image creates and uses a non-root `appuser` (UID 1000) for container security.

---

## 16. Project Statistics

| Metric                         | Count                             |
| ------------------------------ | --------------------------------- |
| Total Python source files      | 24                                |
| API endpoints                  | 11                                |
| Database tables                | 2                                 |
| SQLAlchemy models              | 2 (User, ChessGame)               |
| Pydantic schema classes        | 9                                 |
| Service classes                | 2 (AuthService, ChessGameService) |
| Service methods                | 11                                |
| Python dependencies            | 12                                |
| Documentation files            | 8                                 |
| Database indexes               | 6                                 |
| Alembic migrations             | 1                                 |
| Lines of Python code (approx.) | ~1,500                            |

---

## 17. How to Run

### Option A: Docker Compose (Recommended)

```bash
# 1. Clone / navigate to project
cd d:\Chronica-Backend

# 2. Start all services
docker-compose up -d

# 3. Run migrations
docker-compose exec api alembic upgrade head

# 4. Access
#    API docs:   http://localhost:8000/api/docs
#    Health:     http://localhost:8000/health
#    DB GUI:     http://localhost:8080
```

### Option B: Local Setup (Windows)

```bat
REM 1. Run setup script
setup.bat

REM 2. Edit .env with your PostgreSQL credentials
notepad .env

REM 3. Activate virtual environment
venv\Scripts\activate

REM 4. Run migrations
alembic upgrade head

REM 5. Start server
python -m app.main
REM OR: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option C: Local Setup (Unix/macOS)

```bash
# 1. Run setup script
./setup.sh

# 2. Edit .env
nano .env

# 3. Activate venv
source venv/bin/activate

# 4. Run migrations
alembic upgrade head

# 5. Start
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verifying the Setup

```bash
# Health check
curl http://localhost:8000/health

# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "password123"}'

# Open interactive API docs
# http://localhost:8000/api/docs
```

---

_This document was auto-generated from full static analysis of the Chronica Backend codebase on 2026-06-03._
