#!/bin/bash

# Stock Analysis Platform - Setup Script
# This script sets up the entire development environment

set -e

echo "========================================="
echo "Stock Analysis Platform - Setup"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.10 or higher.${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python version: $PYTHON_VERSION"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker is not installed. Docker is recommended for easy setup.${NC}"
    echo "You can install Docker from: https://docs.docker.com/get-docker/"
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose is not installed.${NC}"
fi

echo ""
echo "Select setup method:"
echo "1) Docker (Recommended - sets up everything automatically)"
echo "2) Local (Manual setup - requires PostgreSQL, Redis)"
echo ""
read -p "Enter choice [1-2]: " choice

case $choice in
    1)
        echo -e "${GREEN}Setting up with Docker...${NC}"

        # Create .env file if it doesn't exist
        if [ ! -f backend/.env ]; then
            echo "Creating backend/.env file..."
            cp backend/.env.example backend/.env
            echo -e "${YELLOW}Please edit backend/.env and configure your settings${NC}"
        fi

        # Build and start containers
        echo "Building Docker containers..."
        docker-compose build

        echo "Starting containers..."
        docker-compose up -d

        # Wait for database to be ready
        echo "Waiting for database to be ready..."
        sleep 5

        # Run migrations
        echo "Running database migrations..."
        docker-compose exec backend alembic upgrade head

        echo ""
        echo -e "${GREEN}Setup complete!${NC}"
        echo ""
        echo "Services:"
        echo "  - Backend API: http://localhost:8000"
        echo "  - API Docs: http://localhost:8000/docs"
        echo "  - Flower (Celery monitoring): http://localhost:5555"
        echo "  - PostgreSQL: localhost:5432"
        echo "  - Redis: localhost:6379"
        echo ""
        echo "To view logs: docker-compose logs -f"
        echo "To stop: docker-compose down"
        ;;

    2)
        echo -e "${GREEN}Setting up locally...${NC}"

        # Check for PostgreSQL
        if ! command -v psql &> /dev/null; then
            echo -e "${RED}PostgreSQL is not installed. Please install PostgreSQL 14+${NC}"
            exit 1
        fi

        # Check for Redis
        if ! command -v redis-cli &> /dev/null; then
            echo -e "${RED}Redis is not installed. Please install Redis 7+${NC}"
            exit 1
        fi

        # Create virtual environment
        echo "Creating Python virtual environment..."
        cd backend
        python3 -m venv venv

        # Activate virtual environment
        echo "Activating virtual environment..."
        source venv/bin/activate

        # Install dependencies
        echo "Installing Python dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt

        # Create .env file
        if [ ! -f .env ]; then
            echo "Creating .env file..."
            cp .env.example .env
            echo -e "${YELLOW}Please edit backend/.env and configure your database settings${NC}"
            echo "Press Enter when ready to continue..."
            read
        fi

        # Create database
        echo "Please create a PostgreSQL database named 'stockanalysis'"
        echo "Example: createdb stockanalysis"
        echo "Press Enter when done..."
        read

        # Run migrations
        echo "Running database migrations..."
        alembic upgrade head

        echo ""
        echo -e "${GREEN}Setup complete!${NC}"
        echo ""
        echo "To start the backend:"
        echo "  cd backend"
        echo "  source venv/bin/activate"
        echo "  uvicorn app.main:app --reload"
        echo ""
        echo "To start Celery worker:"
        echo "  celery -A app.celery_app worker --loglevel=info"
        echo ""
        echo "To start Celery beat:"
        echo "  celery -A app.celery_app beat --loglevel=info"
        ;;

    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "Next Steps:"
echo "========================================="
echo "1. Review and update backend/.env configuration"
echo "2. Access API docs at http://localhost:8000/docs"
echo "3. Create a user account via /api/v1/auth/register"
echo "4. Start using the API!"
echo ""
echo "For more information, see README.md"
echo ""
