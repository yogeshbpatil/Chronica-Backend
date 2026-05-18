# Chronica Backend - API Documentation

Complete API reference for all endpoints with examples.

## Base URL

**Development:** `http://localhost:8000`  
**API Prefix:** `/api/v1`

## Authentication

Protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

Tokens are obtained from `/auth/register` or `/auth/login` endpoints.

**Token Expiration:** 7 days (10080 minutes)

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /api/v1/auth/register`

**Request Body:**

```json
{
  "name": "string (1-80 chars, required)",
  "email": "string (valid email, required)",
  "password": "string (min 8 chars, max 100, required)"
}
```

**Response:** `201 Created`

```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2026-05-17T10:30:00"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJleHAiOjE3MTkwODU4MDB9.signature",
  "expires_at": "2026-05-24T10:30:00"
}
```

**Errors:**

- `400 Bad Request` - Invalid email format or email already exists
- `422 Unprocessable Entity` - Validation error

**Example cURL:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

---

### Login User

Authenticate with email and password.

**Endpoint:** `POST /api/v1/auth/login`

**Request Body:**

```json
{
  "email": "string (valid email, required)",
  "password": "string (required)"
}
```

**Response:** `200 OK`

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

**Errors:**

- `401 Unauthorized` - Invalid credentials
- `422 Unprocessable Entity` - Validation error

**Example cURL:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

---

### Logout User

Clear user session (primarily for frontend cleanup).

**Endpoint:** `POST /api/v1/auth/logout`

**Headers:** None required

**Response:** `200 OK`

```json
{
  "message": "Logged out successfully"
}
```

**Note:** JWT tokens are stateless. This endpoint is mainly for frontend cleanup operations. The token remains valid until expiration.

---

## Chess Games Endpoints

All chess game endpoints require authentication.

### List All Games

Get all chess games for the current user.

**Endpoint:** `GET /api/v1/chess-games`

**Headers:**

```
Authorization: Bearer <token>
```

**Response:** `200 OK`

```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440111",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Tournament Round 3",
    "opponent": "Magnus Carlsen",
    "result": "win",
    "opening": "Sicilian Defense",
    "notes": "Great preparation in opening",
    "created_at": "2026-05-17T10:35:00",
    "updated_at": "2026-05-17T10:35:00"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440112",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Casual Game",
    "opponent": "Friend",
    "result": "draw",
    "opening": "Italian Game",
    "notes": "Interesting endgame",
    "created_at": "2026-05-16T15:20:00",
    "updated_at": "2026-05-16T15:20:00"
  }
]
```

**Errors:**

- `401 Unauthorized` - Invalid or expired token

**Example cURL:**

```bash
curl -X GET "http://localhost:8000/api/v1/chess-games" \
  -H "Authorization: Bearer <token>"
```

---

### Create Chess Game

Record a new chess game.

**Endpoint:** `POST /api/v1/chess-games`

**Headers:**

```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "string (1-120 chars, required)",
  "opponent": "string (1-100 chars, required)",
  "result": "win | loss | draw (required)",
  "opening": "string (0-120 chars, optional)",
  "notes": "string (0-8000 chars, optional)"
}
```

**Response:** `201 Created`

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440113",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Tournament Round 3",
  "opponent": "Magnus Carlsen",
  "result": "win",
  "opening": "Sicilian Defense",
  "notes": "Great preparation in opening",
  "created_at": "2026-05-17T10:35:00",
  "updated_at": "2026-05-17T10:35:00"
}
```

**Errors:**

- `401 Unauthorized` - Invalid or expired token
- `422 Unprocessable Entity` - Validation error
- `404 Not Found` - User not found

**Example cURL:**

```bash
curl -X POST "http://localhost:8000/api/v1/chess-games" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tournament Round 3",
    "opponent": "Magnus Carlsen",
    "result": "win",
    "opening": "Sicilian Defense",
    "notes": "Great preparation in opening"
  }'
```

---

### Get Game Statistics

Get statistics for all games (wins, losses, draws, win rate).

**Endpoint:** `GET /api/v1/chess-games/stats`

**Headers:**

```
Authorization: Bearer <token>
```

**Response:** `200 OK`

```json
{
  "total": 25,
  "wins": 15,
  "losses": 5,
  "draws": 5,
  "win_rate": 60.0
}
```

**Example cURL:**

```bash
curl -X GET "http://localhost:8000/api/v1/chess-games/stats" \
  -H "Authorization: Bearer <token>"
```

---

### Get Recent Games

Get the most recent games (useful for dashboard).

**Endpoint:** `GET /api/v1/chess-games/recent?limit=5`

**Query Parameters:**

- `limit` (integer, default: 5, min: 1, max: 50) - Number of recent games to return

**Headers:**

```
Authorization: Bearer <token>
```

**Response:** `200 OK`

```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440113",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Tournament Round 3",
    "opponent": "Magnus Carlsen",
    "result": "win",
    "opening": "Sicilian Defense",
    "notes": "Great preparation",
    "created_at": "2026-05-17T10:35:00",
    "updated_at": "2026-05-17T10:35:00"
  }
]
```

**Example cURL:**

```bash
curl -X GET "http://localhost:8000/api/v1/chess-games/recent?limit=5" \
  -H "Authorization: Bearer <token>"
```

---

### Get Single Game

Get a specific game by ID.

**Endpoint:** `GET /api/v1/chess-games/{game_id}`

**Path Parameters:**

- `game_id` (string, UUID) - The game ID

**Headers:**

```
Authorization: Bearer <token>
```

**Response:** `200 OK`

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440113",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Tournament Round 3",
  "opponent": "Magnus Carlsen",
  "result": "win",
  "opening": "Sicilian Defense",
  "notes": "Great preparation in opening. Key moment was move 25.",
  "created_at": "2026-05-17T10:35:00",
  "updated_at": "2026-05-17T10:35:00"
}
```

**Errors:**

- `401 Unauthorized` - Invalid or expired token
- `404 Not Found` - Game not found or not owned by user

**Example cURL:**

```bash
curl -X GET "http://localhost:8000/api/v1/chess-games/660e8400-e29b-41d4-a716-446655440113" \
  -H "Authorization: Bearer <token>"
```

---

### Update Chess Game

Update a game record (all fields optional).

**Endpoint:** `PATCH /api/v1/chess-games/{game_id}`

**Path Parameters:**

- `game_id` (string, UUID) - The game ID

**Headers:**

```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body (all fields optional):**

```json
{
  "title": "string (1-120 chars)",
  "opponent": "string (1-100 chars)",
  "result": "win | loss | draw",
  "opening": "string (0-120 chars)",
  "notes": "string (0-8000 chars)"
}
```

**Response:** `200 OK`

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440113",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Tournament Round 3 - UPDATED",
  "opponent": "Magnus Carlsen",
  "result": "win",
  "opening": "Sicilian Defense",
  "notes": "Updated notes",
  "created_at": "2026-05-17T10:35:00",
  "updated_at": "2026-05-17T11:00:00"
}
```

**Errors:**

- `401 Unauthorized` - Invalid or expired token
- `404 Not Found` - Game not found or not owned by user
- `422 Unprocessable Entity` - Validation error

**Example cURL:**

```bash
curl -X PATCH "http://localhost:8000/api/v1/chess-games/660e8400-e29b-41d4-a716-446655440113" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Updated analysis after further study"
  }'
```

---

### Delete Chess Game

Delete a game record.

**Endpoint:** `DELETE /api/v1/chess-games/{game_id}`

**Path Parameters:**

- `game_id` (string, UUID) - The game ID

**Headers:**

```
Authorization: Bearer <token>
```

**Response:** `204 No Content`

**Errors:**

- `401 Unauthorized` - Invalid or expired token
- `404 Not Found` - Game not found or not owned by user

**Example cURL:**

```bash
curl -X DELETE "http://localhost:8000/api/v1/chess-games/660e8400-e29b-41d4-a716-446655440113" \
  -H "Authorization: Bearer <token>"
```

---

## Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "environment": "development",
  "api_version": "1.0.0"
}
```

---

## Error Responses

### Validation Error (422)

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### Unauthorized Error (401)

```json
{
  "detail": "Invalid authentication credentials"
}
```

### Not Found Error (404)

```json
{
  "detail": "Game not found"
}
```

### Bad Request Error (400)

```json
{
  "detail": "An account with this email already exists."
}
```

---

## Response Status Codes

| Code  | Meaning                                               |
| ----- | ----------------------------------------------------- |
| `200` | OK - Request successful                               |
| `201` | Created - Resource created successfully               |
| `204` | No Content - Request successful, no content to return |
| `400` | Bad Request - Invalid request data                    |
| `401` | Unauthorized - Authentication required or invalid     |
| `404` | Not Found - Resource not found                        |
| `422` | Unprocessable Entity - Validation error               |
| `500` | Internal Server Error - Server error                  |

---

## Rate Limiting

Currently not implemented. Will be added in future versions.

---

## CORS Policy

The API accepts requests from:

- `http://localhost:5173` (Vue frontend dev server)
- `http://localhost:3000` (Alternative dev server)
- Production origins (configurable in `.env`)

---

## Testing in Swagger UI

Visit **http://localhost:8000/api/docs** for an interactive API explorer where you can:

1. Test all endpoints
2. View request/response schemas
3. See example values
4. Try authentication workflows

---

## Integration with Frontend

The Vue frontend expects:

1. JWT tokens from auth endpoints
2. Snake_case → camelCase conversion (handled by backend)
3. ISO 8601 datetime format (handled by Pydantic)
4. Consistent error messages

Configure frontend `.env`:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## Debugging

Enable debug logging:

```bash
uvicorn app.main:app --reload --log-level debug
```

View SQL queries:
Set `DEBUG=True` in `.env` to see all SQL statements in console.

---

Last Updated: May 17, 2026
