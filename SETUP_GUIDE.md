# Complete Setup Guide

Step-by-step guide to get the Stock Analysis Platform running.

## Prerequisites

- Docker & Docker Compose (Recommended)
- OR Python 3.10+, PostgreSQL, Redis, Node.js 18+

## Quick Start with Docker (Recommended)

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd data_terminal
```

### 2. Environment Setup
```bash
# Copy environment file
cp backend/.env.example backend/.env

# Edit if needed (optional for local development)
nano backend/.env
```

### 3. Build and Start
```bash
# Build all containers
docker-compose build

# Start all services
docker-compose up -d
```

### 4. Initialize Database
```bash
# Run database initialization (creates tables, admin user, sample data)
./init-db.sh

# OR manually inside the container
docker-compose exec backend python -m app.seed
```

### 5. Access the Platform

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **Flower (Task Monitor)**: http://localhost:5555

### 6. Login

**Default Admin Credentials:**
- Email: `admin@stockanalysis.com`
- Username: `admin`
- Password: `admin123`

**⚠️ IMPORTANT:** Change the admin password immediately after first login!

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
nano .env  # Configure your database

# Create PostgreSQL database
createdb stockanalysis

# Run migrations
alembic upgrade head

# Seed database (creates admin user)
python -m app.seed

# Start backend
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.local.example .env.local

# Start development server
npm run dev
```

### Start Background Workers

```bash
# Terminal 1 - Celery Worker
cd backend
celery -A app.celery_app worker --loglevel=info

# Terminal 2 - Celery Beat (Scheduler)
celery -A app.celery_app beat --loglevel=info

# Terminal 3 - Flower (Optional - Monitoring)
celery -A app.celery_app flower
```

## Creating Additional Admin Users

### Method 1: Interactive Script
```bash
cd backend
python create_admin.py
```

### Method 2: Using API
```bash
# 1. Register a normal user via API or frontend
# 2. Manually update in database
psql stockanalysis
UPDATE users SET is_superuser = true WHERE username = 'yourusername';
```

### Method 3: Via Python Shell
```python
from app.core.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()
admin = User(
    email="newadmin@example.com",
    username="newadmin",
    hashed_password=pwd_context.hash("password123"),
    full_name="New Admin",
    is_superuser=True
)
db.add(admin)
db.commit()
print("Admin created!")
```

## Verifying Installation

### Check Services
```bash
# Check all containers are running
docker-compose ps

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Test Backend API
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}

# Check API docs
# Open: http://localhost:8000/docs
```

### Test Frontend
```bash
# Open browser: http://localhost:3000
# You should see the landing page
```

## Initial Data

After running the seed script, you'll have:

1. **Admin User**
   - Email: admin@stockanalysis.com
   - Username: admin
   - Password: admin123

2. **Sample Companies** (for testing):
   - RELIANCE - Reliance Industries
   - TCS - Tata Consultancy Services
   - HDFCBANK - HDFC Bank
   - INFY - Infosys
   - ICICIBANK - ICICI Bank

## Common Issues

### Port Already in Use
```bash
# Find and kill process using port
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

### Database Connection Error
```bash
# Make sure PostgreSQL is running
docker-compose ps postgres

# Check database URL in .env
cat backend/.env | grep DATABASE_URL
```

### Redis Connection Error
```bash
# Make sure Redis is running
docker-compose ps redis

# Test Redis connection
redis-cli ping
```

### Frontend Can't Connect to Backend
```bash
# Check NEXT_PUBLIC_API_URL in frontend/.env.local
echo $NEXT_PUBLIC_API_URL

# Should be: http://localhost:8000
```

## Development Workflow

### Making Changes

**Backend:**
```bash
# Backend automatically reloads on file changes
docker-compose logs -f backend
```

**Frontend:**
```bash
# Frontend automatically reloads
docker-compose logs -f frontend
```

### Adding New Dependencies

**Backend:**
```bash
# Add to requirements.txt
docker-compose build backend
docker-compose up -d backend
```

**Frontend:**
```bash
# Inside container or locally
cd frontend
npm install <package-name>
docker-compose restart frontend
```

### Database Migrations

```bash
# Create migration after model changes
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec backend alembic upgrade head
```

## Production Deployment

### Environment Variables

Update these in production:

```bash
# Backend (.env)
SECRET_KEY=<generate-strong-random-key>
DEBUG=False
ENVIRONMENT=production
DATABASE_URL=<production-db-url>

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Security Checklist

- [ ] Change admin password
- [ ] Use strong SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Use HTTPS
- [ ] Configure CORS properly
- [ ] Use production database
- [ ] Set up backups
- [ ] Configure monitoring

## Useful Commands

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v

# Rebuild specific service
docker-compose build backend

# View logs
docker-compose logs -f [service-name]

# Execute command in container
docker-compose exec backend python -m app.seed

# Database shell
docker-compose exec postgres psql -U stockuser -d stockanalysis

# Redis shell
docker-compose exec redis redis-cli
```

## Next Steps

1. Login with admin credentials
2. Change admin password in Settings
3. Explore the Stock Screener
4. Search for companies
5. Create a portfolio
6. Set up alerts
7. Start analyzing stocks!

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Review [CONTRIBUTING.md](CONTRIBUTING.md)
- Open a GitHub issue

---

**Happy Analyzing!** 📊📈
