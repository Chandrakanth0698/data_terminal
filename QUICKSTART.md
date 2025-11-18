# Quick Start Guide

Get started with the Stock Analysis Platform in 5 minutes!

## Option 1: Docker (Recommended)

### Prerequisites
- Docker
- Docker Compose

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/data_terminal.git
cd data_terminal

# 2. Create environment file
cp backend/.env.example backend/.env

# 3. Start all services
docker-compose up -d

# 4. Run database migrations
docker-compose exec backend alembic upgrade head

# 5. Access the application
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# Flower: http://localhost:5555
```

That's it! The platform is now running.

## Option 2: Local Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis 7+

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/data_terminal.git
cd data_terminal/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 5. Create database
createdb stockanalysis

# 6. Run migrations
alembic upgrade head

# 7. Start the server
uvicorn app.main:app --reload
```

## First Steps

### 1. Create a User Account

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "securepassword",
    "full_name": "Test User"
  }'
```

### 2. Login and Get Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepassword"
```

Save the `access_token` from the response.

### 3. Search for Companies

```bash
curl "http://localhost:8000/api/v1/companies/search?query=RELIANCE" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Run a Stock Screen

```bash
curl -X POST "http://localhost:8000/api/v1/screener/screen" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "market_cap": {"min": 1000},
      "pe_ratio": {"max": 25},
      "roe": {"min": 15}
    },
    "limit": 10
  }'
```

### 5. Get Financial Data

```bash
curl "http://localhost:8000/api/v1/financial/RELIANCE/statements?years=5" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Using the Interactive API Docs

The easiest way to explore the API is through the interactive documentation:

1. Open http://localhost:8000/docs in your browser
2. Click "Authorize" and enter your access token
3. Try out different endpoints directly from the browser

## Next Steps

- **Explore Preset Screens**: Try `/api/v1/screener/presets` to see pre-configured strategies
- **Create a Portfolio**: Use `/api/v1/portfolio` endpoints to track your holdings
- **Set Up Alerts**: Configure price and ratio alerts at `/api/v1/alerts`
- **Valuation Models**: Build DCF models at `/api/v1/valuation`

## Common Issues

### Database Connection Error
- Make sure PostgreSQL is running
- Check DATABASE_URL in `.env` file
- Verify database exists: `psql -l | grep stockanalysis`

### Redis Connection Error
- Make sure Redis is running: `redis-cli ping`
- Check REDIS_URL in `.env` file

### Module Import Errors
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

## Development Mode

### Start Backend with Auto-Reload
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Celery Worker
```bash
celery -A app.celery_app worker --loglevel=info
```

### Start Celery Beat (Scheduler)
```bash
celery -A app.celery_app beat --loglevel=info
```

### Monitor Celery Tasks
```bash
celery -A app.celery_app flower
# Open http://localhost:5555
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment instructions.

## Getting Help

- **Documentation**: Check [README.md](README.md) for detailed information
- **API Reference**: http://localhost:8000/docs
- **Issues**: Open an issue on GitHub
- **Discussions**: Join GitHub Discussions

---

Happy analyzing! 📊
