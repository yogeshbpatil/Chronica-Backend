# Chronica Backend - Architecture Guide

A detailed guide to the backend architecture and design patterns used in this project.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Vue 3 Frontend                           │
│                  (localhost:5173)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                    HTTP/REST
                    (Axios)
                         │
         ┌───────────────┴───────────────┐
         │                               │
┌────────▼────────────────────────────────────────────────────┐
│                 FastAPI Backend                             │
│               (localhost:8000)                              │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         API Layer (FastAPI Routes)                   │  │
│  │  ├─ /api/v1/auth/register (POST)                    │  │
│  │  ├─ /api/v1/auth/login (POST)                       │  │
│  │  ├─ /api/v1/chess-games (GET, POST)                │  │
│  │  ├─ /api/v1/chess-games/{id} (GET, PATCH, DELETE) │  │
│  │  └─ /api/v1/chess-games/stats (GET)                │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐  │
│  │    Dependency Injection & Authentication             │  │
│  │  ├─ get_current_user (JWT validation)                │  │
│  │  ├─ get_db (database session)                        │  │
│  │  └─ get_settings (configuration)                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐  │
│  │      Services Layer (Business Logic)                 │  │
│  │  ├─ AuthService                                      │  │
│  │  │  ├─ register()                                    │  │
│  │  │  ├─ login()                                       │  │
│  │  │  └─ get_user_by_id()                              │  │
│  │  └─ ChessGameService                                 │  │
│  │     ├─ create_game()                                 │  │
│  │     ├─ get_all_games()                               │  │
│  │     ├─ get_game_by_id()                              │  │
│  │     ├─ update_game()                                 │  │
│  │     ├─ delete_game()                                 │  │
│  │     └─ get_game_stats()                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐  │
│  │    Data Access Layer (ORM)                           │  │
│  │  ├─ User Model (SQLAlchemy)                          │  │
│  │  └─ ChessGame Model (SQLAlchemy)                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
└─────────────────────────┼─────────────────────────────────────┘
                          │
                   PostgreSQL
                    (Database)
```

## Layered Architecture

### 1. **API Layer** (`app/api/v1/endpoints/`)

**Responsibility:** Handle HTTP requests and responses

```python
# Example endpoint structure
@router.post("/chess-games")
async def create_game(
    game_data: ChessGameCreate,  # Pydantic validation
    current_user: User = Depends(get_current_user),  # Authentication
    db: Session = Depends(get_db)  # Database session
) -> ChessGameResponse:
    service = ChessGameService(db)
    return service.create_game(current_user.id, game_data)
```

**Files:**

- `endpoints/auth.py` - Authentication endpoints
- `endpoints/chess_games.py` - Chess games CRUD endpoints

**Pattern:** Thin controllers - delegate to services

---

### 2. **Service Layer** (`app/services/`)

**Responsibility:** Implement business logic

```python
# Example service structure
class ChessGameService:
    def __init__(self, db: Session):
        self.db = db

    def create_game(self, user_id: str, game_data: ChessGameCreate) -> ChessGameResponse:
        # Validate user exists
        # Create game
        # Return response
        pass
```

**Files:**

- `auth.py` - Authentication business logic
- `chess_game.py` - Chess games business logic

**Pattern:** Services handle all business rules and data manipulation

---

### 3. **Data Access Layer** (`app/db/`, `app/models/`)

**Responsibility:** Database operations via ORM

```python
# SQLAlchemy Models
class User(Base):
    __tablename__ = "users"
    id: str
    email: str
    # relationships, etc.

class ChessGame(Base):
    __tablename__ = "chess_games"
    id: str
    user_id: str  # Foreign key
    title: str
    # etc.
```

**Files:**

- `db/database.py` - Database configuration and sessions
- `models/models.py` - SQLAlchemy ORM models

**Pattern:** Direct database access through SQLAlchemy ORM

---

### 4. **Validation Layer** (`app/schemas/`)

**Responsibility:** Request/response validation using Pydantic

```python
# Pydantic Schemas
class ChessGameCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    opponent: str = Field(..., min_length=1, max_length=100)
    result: GameResultEnum
    opening: str = Field(default="", max_length=120)
    notes: str = Field(default="", max_length=8000)
```

**Files:**

- `schemas/auth.py` - Auth request/response models
- `schemas/chess_game.py` - Game request/response models

**Pattern:** Automatic validation and serialization

---

### 5. **Security Layer** (`app/core/security.py`)

**Responsibility:** Password hashing, JWT token management

```python
class SecurityUtils:
    @staticmethod
    def hash_password(password: str) -> str
    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool
    @staticmethod
    def create_access_token(data: dict) -> str
    @staticmethod
    def decode_token(token: str) -> dict
```

**Pattern:** Centralized security operations

---

### 6. **Dependency Injection** (`app/utils/dependencies.py`)

**Responsibility:** Extract and validate current user from JWT

```python
def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    # Decode JWT
    # Fetch user from database
    # Return user object
    pass
```

**Pattern:** FastAPI dependencies for reusable logic

---

## Data Flow Examples

### Authentication Flow

```
1. User submits LoginRequest
   └─> FastAPI validates with Pydantic (LoginRequest schema)

2. Endpoint receives request
   └─> router.post("/auth/login", response_model=AuthSessionResponse)

3. Service handles business logic
   └─> AuthService.login(credentials)
       ├─ Query database for user (SQLAlchemy)
       ├─ Verify password (SecurityUtils.verify_password)
       └─ Create JWT token (SecurityUtils.create_access_token)

4. Response serialized and sent
   └─> AuthSessionResponse (contains user, token, expires_at)

5. Frontend stores token in localStorage
   └─> Includes in Authorization header for future requests
```

### Chess Game CRUD Flow

```
CREATE GAME:
1. POST /api/v1/chess-games with ChessGameCreate
   └─> Pydantic validates request body

2. get_current_user dependency extracts user from JWT
   └─> SecurityUtils.decode_token(token)
   └─> Database query for user

3. ChessGameService.create_game(user_id, game_data)
   └─> Verify user exists
   └─> Create ChessGame model instance
   └─> Commit to database
   └─> Return ChessGameResponse

4. Response returned to frontend

READ GAMES:
1. GET /api/v1/chess-games
   └─> Current user extracted via dependency

2. ChessGameService.get_all_games(user_id)
   └─> Query database: SELECT * FROM chess_games WHERE user_id = ?
   └─> Return list of ChessGameResponse objects

UPDATE GAME:
1. PATCH /api/v1/chess-games/{game_id} with ChessGameUpdate
   └─> Current user extracted
   └─> Game_id from URL path

2. ChessGameService.update_game(user_id, game_id, game_data)
   └─> Query database with user ownership check
   └─> Update only provided fields
   └─> Commit changes
   └─> Return updated ChessGameResponse

DELETE GAME:
1. DELETE /api/v1/chess-games/{game_id}
   └─> Current user extracted

2. ChessGameService.delete_game(user_id, game_id)
   └─> Query database with ownership check
   └─> Delete game
   └─> Commit
   └─> Return 204 No Content
```

## Design Patterns Used

### 1. **Dependency Injection**

```python
# FastAPI injects dependencies
async def create_game(
    game_data: ChessGameCreate = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pass
```

### 2. **Service Pattern**

```python
# Services encapsulate business logic
class ChessGameService:
    def __init__(self, db: Session):
        self.db = db

    def create_game(self, ...): ...
    def get_all_games(self, ...): ...
```

### 3. **Repository Pattern** (implicit through SQLAlchemy)

```python
# All database queries through ORM
user = db.query(User).filter(User.id == user_id).first()
games = db.query(ChessGame).filter(ChessGame.user_id == user_id).all()
```

### 4. **Factory Pattern**

```python
# create_app() factory creates configured FastAPI instance
app = create_app()
```

### 5. **Middleware Pattern**

```python
# CORS, exception handling as middleware
app.add_middleware(CORSMiddleware, ...)
app.exception_handler(RequestValidationError)
```

## Security Architecture

### Authentication Flow

```
┌─────────────────────────────────────────────┐
│         Client (Vue Frontend)               │
└────────────────┬────────────────────────────┘
                 │
         1. Login with email/password
                 │
┌────────────────▼────────────────────────────┐
│      FastAPI - POST /auth/login             │
├─────────────────────────────────────────────┤
│  2. Validate Pydantic schema                 │
│  3. Query database for user                  │
│  4. Hash password verification               │
│  5. Generate JWT (HS256)                     │
│  6. Return token + expiration                │
└────────────────┬────────────────────────────┘
                 │
         7. Store token in localStorage
                 │
┌────────────────▼────────────────────────────┐
│   Subsequent Requests with Bearer Token    │
│   Authorization: Bearer <JWT_TOKEN>         │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│  FastAPI - get_current_user Dependency     │
├─────────────────────────────────────────────┤
│  1. Extract token from Authorization header │
│  2. Decode JWT (verify signature)           │
│  3. Extract user_id from payload            │
│  4. Query database for user                 │
│  5. Return User object or raise 401         │
└────────────────┬────────────────────────────┘
                 │
          6. User accessible in endpoint
```

### Password Security

```python
# Bcrypt hashing with configurable cost factor
password_hash = pwd_context.hash(plain_password)
is_valid = pwd_context.verify(plain_password, password_hash)

# Never store plain passwords
# Passwords hashed at registration and login
# Verification is constant-time comparison
```

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW()
);
```

### Chess Games Table

```sql
CREATE TABLE chess_games (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(120) NOT NULL,
    opponent VARCHAR(100) NOT NULL,
    result ENUM('win', 'loss', 'draw') NOT NULL,
    opening VARCHAR(120),
    notes TEXT,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_chess_games_user_id ON chess_games(user_id);
CREATE INDEX idx_chess_games_created_at ON chess_games(created_at DESC);
CREATE INDEX idx_chess_games_result ON chess_games(result);
```

## Error Handling

### Exception Hierarchy

```
HTTPException (FastAPI)
├─ 400 Bad Request (validation errors, duplicate resources)
├─ 401 Unauthorized (invalid/expired token)
├─ 404 Not Found (resource not found)
├─ 422 Unprocessable Entity (validation errors)
└─ 500 Internal Server Error (unexpected errors)
```

### Error Response Format

```python
# Validation errors
{
    "detail": [
        {
            "loc": ["body", "email"],
            "msg": "value is not a valid email",
            "type": "value_error.email"
        }
    ]
}

# Custom errors
{
    "detail": "An account with this email already exists."
}
```

## Configuration Management

### Environment Variables

```
DATABASE_URL          # PostgreSQL connection string
SECRET_KEY            # JWT signing key
ALGORITHM             # JWT algorithm (HS256)
ACCESS_TOKEN_EXPIRE_MINUTES  # Token lifespan (7 days = 10080)
DEBUG                 # Enable debug logging
ENVIRONMENT           # dev/staging/production
BACKEND_CORS_ORIGINS  # Allowed CORS origins
```

### Settings Class

```python
class Settings(BaseSettings):
    # All settings loaded from environment
    # Type-safe with Pydantic
    # Cached with @lru_cache()

settings = get_settings()  # Singleton
```

## Performance Considerations

### Database Indexing

```python
# Indexes for common queries
id = Column(..., primary_key=True)  # Implicit index
user_id = Column(..., index=True)   # User's games lookup
created_at = Column(..., index=True)  # Recent games
email = Column(..., unique=True)    # Login lookup
```

### Query Optimization

```python
# Eager loading relationships (future)
# Pagination (future)
# Caching with Redis (future)
# Connection pooling (automatic with SQLAlchemy)
```

## Scalability Path

### Phase 1: MVP (Current)

- Single PostgreSQL instance
- In-memory JWT validation
- No caching

### Phase 2: Growth

- Add Redis for caching
- Implement pagination
- Add database connection pooling
- Rate limiting

### Phase 3: Enterprise

- Multiple database replicas
- Message queue (Celery)
- Distributed caching
- Microservices architecture

## Testing Strategy (Future)

```
Unit Tests
├─ Services (business logic)
├─ Schemas (validation)
└─ Security utils

Integration Tests
├─ Auth endpoints
├─ Chess games endpoints
└─ Database operations

End-to-End Tests
├─ Full workflows
└─ API contracts
```

## Deployment Architecture

### Local Development

```
Docker Compose
├─ FastAPI (hot reload)
├─ PostgreSQL
└─ Adminer (GUI)
```

### Staging/Production

```
Render (FastAPI)  ←→  Neon PostgreSQL
```

## Contributing

When adding new features:

1. Create model in `models/models.py`
2. Create schemas in `schemas/`
3. Create service in `services/`
4. Create endpoints in `api/v1/endpoints/`
5. Create migration (if needed)
6. Add tests (future)
7. Update documentation

---

**Last Updated:** May 17, 2026  
**Version:** 1.0.0
