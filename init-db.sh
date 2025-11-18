#!/bin/bash

# Initialize Database Script
# Creates tables, admin user, and sample data

set -e

echo "========================================="
echo "Database Initialization"
echo "========================================="
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "⚠️  Warning: backend/.env not found"
    echo "Creating from .env.example..."
    cp backend/.env.example backend/.env
    echo "✓ Created backend/.env"
    echo ""
fi

# Check database connection
echo "Checking database connection..."
if command -v psql &> /dev/null; then
    # Extract DB details from .env
    DB_URL=$(grep DATABASE_URL backend/.env | cut -d '=' -f2)
    if [ ! -z "$DB_URL" ]; then
        echo "✓ Database URL found"
    fi
fi

# Run Alembic migrations
echo ""
echo "Running database migrations..."
cd backend
python -m alembic upgrade head
echo "✓ Migrations completed"

# Run seed script
echo ""
echo "Seeding database..."
python -m app.seed
echo "✓ Database seeded"

echo ""
echo "========================================="
echo "Initialization Complete!"
echo "========================================="
echo ""
echo "Default Admin Credentials:"
echo "  Email: admin@stockanalysis.com"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Change the admin password after first login!"
echo ""
echo "You can now start the application:"
echo "  docker-compose up -d"
echo "  OR"
echo "  cd backend && uvicorn app.main:app --reload"
echo ""
