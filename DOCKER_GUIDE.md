# Chronica Backend - Using Docker Compose

This guide explains how to run the Chronica backend using Docker and Docker Compose.

## Prerequisites

- Docker (https://www.docker.com/products/docker-desktop)
- Docker Compose (usually included with Docker Desktop)

## Quick Start

### 1. Start Services

```bash
# From project root directory
docker-compose up -d
```

This will:

- Create and start PostgreSQL container
- Create and start FastAPI application container
- Create and start Adminer (optional database GUI)
- Create a shared network for containers to communicate

### 2. Access Services

- **FastAPI API:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/api/docs
- **Health Check:** http://localhost:8000/health
- **Adminer (Database GUI):** http://localhost:8080

### 3. View Logs

```bash
# View all container logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f postgres
```

### 4. Stop Services

```bash
# Stop all running containers
docker-compose down

# Stop and remove volumes (delete database)
docker-compose down -v
```

## Database Access

### Using Adminer (Web GUI)

Visit **http://localhost:8080**

- Server: `postgres`
- Username: `chronica_user`
- Password: `chronica_password`
- Database: `Chronica_Database`

### Using psql Command Line

```bash
# Connect to database in Docker container
docker exec -it chronica_postgres psql -U chronica_user -d Chronica_Database

# Useful psql commands:
\dt              # List all tables
\d table_name    # Describe table
SELECT * FROM users;  # View users
```

## Development Workflow

### 1. Make Code Changes

- Edit files in your IDE
- Changes are automatically reloaded (hot reload enabled)

### 2. Apply Database Migrations (if needed)

```bash
# Run migrations inside the container
docker-compose exec api alembic upgrade head
```

### 3. Create New Migration (if you modify models)

```bash
docker-compose exec api alembic revision --autogenerate -m "Your migration message"
```

### 4. Run Custom Commands

```bash
# Access app container shell
docker-compose exec api bash

# Inside container:
python -c "from app.db import engine; print('Connected')"
```

## Building and Pushing to Registry

### Build Image

```bash
docker build -t chronica-api:latest .
```

### Tag for Registry

```bash
docker tag chronica-api:latest your-registry/chronica-api:latest
```

### Push to Registry

```bash
docker push your-registry/chronica-api:latest
```

## Production Deployment

### For Render.com

1. Push code to GitHub
2. Create new Web Service on Render
3. Set environment variables:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=your-production-key
   DEBUG=False
   ENVIRONMENT=production
   ```
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### For Neon (Database)

1. Create PostgreSQL database on Neon
2. Use the Neon connection string as `DATABASE_URL`
3. Ensure Render app can access Neon (should work by default)

## Troubleshooting

### Port Already in Use

```bash
# Check which process is using the port
lsof -i :8000

# Or just use different ports in docker-compose.yml:
# Change "8000:8000" to "8001:8000"
```

### Database Connection Failed

```bash
# Check if postgres container is healthy
docker-compose ps

# View postgres logs
docker-compose logs postgres

# Restart postgres
docker-compose restart postgres
```

### Volume Permission Issues (Linux)

```bash
# Fix postgres data directory permissions
sudo chown 1000:1000 -R your-data-directory
```

### Clean Everything and Start Fresh

```bash
docker-compose down -v
docker volume prune
docker-compose up -d
```

## Environment Variables

Edit `docker-compose.yml` under the `api` service `environment` section to change:

- Database credentials
- Secret key
- API configuration
- Debug mode
- CORS origins

## Health Checks

The FastAPI container includes a health check. View status:

```bash
docker inspect chronica_api | grep -A 10 "Health"
```

## Resource Limits (Optional)

Add to `docker-compose.yml` service to limit resources:

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 512M
        reservations:
          cpus: "0.5"
          memory: 256M
```

## Useful Docker Commands

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View container details
docker inspect chronica_api

# Access container shell
docker exec -it chronica_api bash

# View real-time logs
docker logs -f chronica_api

# Restart a service
docker-compose restart api

# Remove unused resources
docker system prune
```

## Switching Between Local and Docker

### Local Development

```bash
# Use .env file with localhost
uvicorn app.main:app --reload
```

### Docker Development

```bash
# Use docker-compose
docker-compose up -d
```

## Next Steps

1. ✅ Backend running in Docker
2. Configure Vue frontend to use `http://localhost:8000/api`
3. Run Vue frontend: `npm run dev`
4. Test full integration
5. Deploy to production when ready

---

For more information, see:

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
