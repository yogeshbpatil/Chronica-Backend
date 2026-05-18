# Chronica Backend - Deployment Guide

Step-by-step guide to deploy the FastAPI backend to Render and PostgreSQL to Neon for free hosting.

## Prerequisites

- GitHub account with code pushed
- Render account (https://render.com) - free tier available
- Neon account (https://neon.tech) - free PostgreSQL hosting

## Step 1: Deploy PostgreSQL on Neon

### 1.1 Create Neon Database

1. Go to https://neon.tech and sign up
2. Click "Create a new project"
3. Select PostgreSQL version (latest)
4. Choose region closest to your users
5. Create project
6. Database will be created automatically

### 1.2 Get Connection String

1. In Neon console, go to "Connection string"
2. Select "Pooled connection" (recommended for serverless)
3. Copy the connection string:
   ```
   postgresql://username:password@host/dbname?sslmode=require
   ```
4. Save this securely - you'll need it for Render

### 1.3 (Optional) Test Connection Locally

```bash
# Update .env with Neon connection string
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# Run migrations
alembic upgrade head

# Or just start the app - tables will auto-create
python -m app.main
```

## Step 2: Deploy FastAPI on Render

### 2.1 Prepare Repository

Ensure your GitHub repository has:

```
Chronica-Backend/
├── app/
├── alembic/
├── requirements.txt
├── .env.example
├── Dockerfile  (optional, but recommended)
└── README.md
```

Commit and push all changes:

```bash
git add .
git commit -m "Initial FastAPI backend setup"
git push origin main
```

### 2.2 Create Render Web Service

1. Go to https://render.com and sign up
2. Connect your GitHub account
3. Click "New +" → "Web Service"
4. Select your Chronica-Backend repository
5. Configure:
   - **Name:** `chronica-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - **Instance Type:** Free tier
   - **Region:** Same as your Neon database region

### 2.3 Set Environment Variables

In Render dashboard:

1. Click on your web service
2. Go to "Environment" tab
3. Add environment variables:

```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
API_TITLE=Chronica API
API_VERSION=1.0.0
API_DESCRIPTION=Personal Knowledge Management Platform Backend
ENVIRONMENT=production
DEBUG=False
BACKEND_CORS_ORIGINS=["https://your-frontend-url.com"]
```

**Important:**

- Generate a strong `SECRET_KEY`: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Update `BACKEND_CORS_ORIGINS` with your actual frontend URL
- Set `DEBUG=False` for production

### 2.4 Deploy

1. Click "Deploy" button
2. Wait for deployment to complete (2-5 minutes)
3. You'll get a URL like: `https://chronica-api.onrender.com`

### 2.5 Verify Deployment

Test your deployed API:

```bash
# Health check
curl https://chronica-api.onrender.com/health

# Access Swagger docs
https://chronica-api.onrender.com/api/docs

# Test registration
curl -X POST "https://chronica-api.onrender.com/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
```

## Step 3: Configure Vue Frontend

Update your Vue frontend `.env.production`:

```
VITE_API_BASE_URL=https://chronica-api.onrender.com/api
```

## Step 4: Continuous Deployment

### Auto-Deploy on Push

Render automatically deploys when you push to your repository:

1. Make changes to code
2. Commit and push: `git push origin main`
3. Render automatically builds and deploys
4. Check deployment status in Render dashboard

### Manual Redeploy

1. Go to Render dashboard
2. Click your web service
3. Click "Manual Deploy"
4. Select branch to deploy

## Step 5: Monitor and Maintain

### View Logs

```bash
# In Render dashboard
1. Click your web service
2. Go to "Logs" tab
3. View real-time logs
```

### Restart Service

```bash
# In Render dashboard
1. Click your web service
2. Click "Restart Service"
```

### View Metrics

```bash
# In Render dashboard
1. Go to "Metrics" tab
2. View CPU, memory, response times
```

### Scale (Upgrade)

```bash
# In Render dashboard
1. Go to "Settings"
2. Click "Upgrade to Paid"
3. Choose instance type
```

## Troubleshooting Deployment

### Database Connection Failed

**Error:** `could not connect to server: Connection refused`

**Solution:**

1. Verify Neon connection string in environment variables
2. Check database is running on Neon
3. Ensure `sslmode=require` in connection string
4. Whitelist Render IP in Neon (if needed)

### Port Configuration Issue

**Error:** `Address already in use`

**Solution:**

- Render automatically assigns port 8000
- Start command should bind to `0.0.0.0:8000`
- This is already configured in `docker-compose.yml`

### CORS Error

**Frontend error:** `No 'Access-Control-Allow-Origin' header`

**Solution:**

1. Update `BACKEND_CORS_ORIGINS` environment variable
2. Include full URL: `https://your-frontend-url.com`
3. Redeploy

### Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**

1. Ensure `requirements.txt` is in project root
2. Build command includes: `pip install -r requirements.txt`
3. All imports are correct

### Timeout Issues

**Error:** `Error: R10 Boot timeout`

**Solution:**

- Render allows 30 seconds to start
- Ensure app starts quickly
- Check logs for startup errors

## Cost Optimization

### Free Tier Limits

**Render:**

- Free web services sleep after 15 minutes of inactivity
- Auto-resume on request (slight delay)
- Limited to 1 free service per account

**Neon:**

- Free PostgreSQL database (up to 3 GB)
- 100 branches for testing
- Automatic backups

### Upgrade to Paid (Optional)

**Render Pricing:**

- ~$7/month for always-on web service
- Better performance, no sleep

**Neon Pricing:**

- $0.30 per compute hour (pay-as-you-go)
- Storage beyond 3GB: $0.19/GB/month

## Backup Strategy

### Neon Automatic Backups

Neon automatically backs up your database daily. To restore:

1. Go to Neon dashboard
2. Select your project
3. Go to "Backups"
4. Restore from backup

### Manual Backup

```bash
# Download database locally
pg_dump -U username -h host -d dbname > backup.sql

# Restore from backup
psql -U username -h host -d dbname < backup.sql
```

## Production Checklist

- [ ] Database created on Neon
- [ ] Environment variables set on Render
- [ ] `SECRET_KEY` changed to strong random value
- [ ] `DEBUG=False` in production
- [ ] `BACKEND_CORS_ORIGINS` set to frontend URL
- [ ] Health check endpoint working
- [ ] API documentation accessible
- [ ] Test user registration works
- [ ] Test login works
- [ ] Test chess games CRUD works
- [ ] Frontend configured with API URL
- [ ] Error logging configured
- [ ] Monitoring set up

## Monitoring and Alerts

### Set Up Alerts (Optional)

1. Go to Render dashboard
2. Click web service → Settings
3. Enable notifications for:
   - Build failure
   - Deployment failure
   - Service crash

### Monitor Performance

View metrics in Render dashboard:

- CPU usage
- Memory usage
- Response time
- Error rate
- Build time

## Scaling Considerations

### When to Upgrade

Upgrade to paid tier if:

- Service frequently sleeps (>15 min inactive)
- High traffic causes slowdowns
- Need guaranteed uptime
- Database exceeds 3GB

### Database Scaling

Neon automatically scales. For larger deployments:

- Monitor compute hour usage
- Consider reserved compute
- Implement caching (Redis)
- Optimize queries

## API Rate Limiting (Future)

For production, implement:

```python
# In requirements.txt
slowapi==0.1.9

# In app/main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/v1/chess-games")
@limiter.limit("30/minute")
async def list_games(...):
    pass
```

## Security Hardening (Production)

### Environment Variables

- ✅ Never commit `.env` (use `.env.example`)
- ✅ Use strong `SECRET_KEY` (32+ characters)
- ✅ Rotate secrets regularly
- ✅ Use HTTPS only (Render handles this)

### Database

- ✅ Use strong PostgreSQL password
- ✅ Enable SSL connections
- ✅ Regular backups (Neon automatic)
- ✅ Monitor unusual queries

### API

- ✅ Set `DEBUG=False`
- ✅ Enable HTTPS only
- ✅ Implement rate limiting
- ✅ Log security events

## Disaster Recovery

### If Render Service Fails

1. Render automatically restarts failed services
2. Check Render dashboard logs
3. Manual restart: Click "Restart Service"
4. Check if issue is:
   - Code error (fix and push)
   - Environment variable (update and redeploy)
   - Database error (check Neon)

### If Neon Database Fails

1. Contact Neon support
2. Check backup availability
3. Restore from backup if needed
4. Verify data integrity

## Performance Optimization

### Database Query Performance

```python
# Use indexes (already configured)
# Limit results (for list endpoints)
# Avoid N+1 queries (use eager loading if needed)

# Example: Get recent games with limit
games = db.query(ChessGame).filter(
    ChessGame.user_id == user_id
).order_by(
    desc(ChessGame.created_at)
).limit(10).all()
```

### API Response Caching

Future improvement - implement caching:

```python
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

@router.get("/chess-games")
@cached(namespace="games", expire=300)
async def list_games(...):
    pass
```

## Support

For issues:

- Render Support: https://render.com/support
- Neon Support: https://neon.tech/contact
- FastAPI Docs: https://fastapi.tiangolo.com/
- GitHub Issues: Create issues in your repository

---

**Deployment Summary:**

1. Create Neon PostgreSQL database (free)
2. Get connection string from Neon
3. Create Render web service
4. Set environment variables
5. Deploy FastAPI backend
6. Update Vue frontend API URL
7. Test and monitor

**Estimated Setup Time:** 15-20 minutes

---

**Last Updated:** May 17, 2026  
**Version:** 1.0.0
