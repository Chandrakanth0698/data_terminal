# Contributing to Stock Analysis Platform

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/data_terminal.git
   cd data_terminal
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**

4. **Test your changes**

5. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (recommended)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Running with Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Project Structure

```
data_terminal/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configs
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── modules/      # Business logic modules
│   │   └── tasks/        # Celery tasks
│   ├── tests/            # Tests
│   └── alembic/          # Database migrations
├── frontend/             # Next.js frontend
├── docs/                 # Documentation
└── docker-compose.yml
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

**Example:**

```python
def calculate_dcf(
    company_id: int,
    projection_years: int = 5,
    wacc: float = 10.0
) -> Dict[str, Any]:
    """
    Calculate DCF valuation for a company.

    Args:
        company_id: Company ID
        projection_years: Number of years to project
        wacc: Weighted Average Cost of Capital (%)

    Returns:
        Dictionary with DCF results

    Raises:
        ValueError: If company not found
    """
    # Implementation
    pass
```

### Code Formatting

We use:
- **Black** for Python code formatting
- **isort** for import sorting
- **flake8** for linting

```bash
# Format code
black .
isort .

# Check linting
flake8 .
```

### Database Migrations

When changing models:

```bash
# Create migration
alembic revision --autogenerate -m "Description of changes"

# Review the migration file in alembic/versions/

# Apply migration
alembic upgrade head
```

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
feat(screener): add support for custom date ranges

Add ability to backtest screener strategies with custom date ranges.
Includes new API endpoint and service layer changes.

Closes #123
```

```bash
fix(dcf): correct terminal value calculation

Terminal value was using wrong growth rate.
Now uses perpetuity growth method correctly.
```

## Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update API documentation

2. **Write Tests**
   - Add unit tests for new features
   - Ensure all tests pass
   - Aim for >80% code coverage

3. **Run Checks**
   ```bash
   # Format code
   black .
   isort .

   # Run tests
   pytest

   # Check coverage
   pytest --cov=app tests/
   ```

4. **Create Pull Request**
   - Use a clear, descriptive title
   - Reference related issues
   - Describe what changed and why
   - Include screenshots for UI changes

5. **Code Review**
   - Address reviewer feedback
   - Keep discussions focused and professional
   - Make requested changes in new commits

6. **Merge**
   - PRs require at least one approval
   - All CI checks must pass
   - Use "Squash and merge" for clean history

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_screener.py

# Run specific test
pytest tests/test_screener.py::test_basic_screen
```

### Writing Tests

```python
import pytest
from app.modules.screener import StockScreener

def test_screener_basic_filters(db_session):
    """Test basic screener functionality"""
    screener = StockScreener(db_session)

    filters = {
        'market_cap': {'min': 1000},
        'pe_ratio': {'max': 25}
    }

    result = screener.screen(filters, limit=10)

    assert result['total_count'] >= 0
    assert len(result['results']) <= 10
    assert result['filters'] == filters
```

## Module Development Guidelines

### Adding a New Module

1. Create module directory under `backend/app/modules/`
2. Create `__init__.py` with exports
3. Implement business logic
4. Create API endpoints in `backend/app/api/endpoints/`
5. Add Pydantic schemas
6. Write tests
7. Update documentation

### Adding a New Data Source

1. Create fetcher class in `app/modules/data_ingestion/`
2. Implement fetch methods
3. Add error handling and logging
4. Create Celery task for scheduled fetching
5. Add configuration to `.env.example`
6. Document the integration

## Documentation

- Use clear, concise language
- Include code examples
- Keep README.md updated
- Add inline comments for complex logic
- Document all API endpoints

## Questions?

- Open an issue for bugs
- Start a discussion for features
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Stock Analysis Platform! 🚀
