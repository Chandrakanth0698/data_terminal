# Stock Analysis & Investment Research Platform

A comprehensive stock analysis platform for Indian markets (NSE/BSE) implementing Richard Coffin's 6-step fundamental analysis process.

## 🎯 Features

### Core Modules
1. **Stock Screener** - Filter stocks by 50+ criteria with backtesting
2. **Business Understanding** - Company overview, SWOT, peers, KPIs
3. **Financial Analysis** - 10+ years statements, 40+ ratios, red flag detection
4. **Strategy Analysis** - Earnings transcripts, sentiment analysis, guidance tracking
5. **Valuation Models** - DCF, relative valuation, sensitivity analysis
6. **Research Notes** - Documentation, watchlists, PDF reports
7. **Portfolio Tracking** - Holdings, returns (XIRR), performance metrics
8. **Alerts & Notifications** - Price alerts, results reminders, threshold alerts

## 🏗️ Tech Stack

### Backend
- **Python 3.10+** - Primary language
- **FastAPI** - REST API framework
- **PostgreSQL** - Relational database
- **Redis** - Caching & session management
- **SQLAlchemy** - ORM
- **Celery** - Background tasks
- **APScheduler** - Scheduled jobs

### Frontend
- **React 18+** - UI framework
- **Next.js** - SSR/SSG capabilities
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **shadcn/ui** - Component library
- **Recharts** - Data visualization
- **TanStack Query** - Data fetching

### Data Sources (Free/Freemium)
- NSE/BSE official websites
- Yahoo Finance
- Screener.in
- Tijori Finance
- Trendlyne
- Google News RSS
- MoneyControl

## 📁 Project Structure

```
data_terminal/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core configs
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── modules/          # Feature modules
│   │   │   ├── screener/
│   │   │   ├── business/
│   │   │   ├── financial/
│   │   │   ├── strategy/
│   │   │   ├── valuation/
│   │   │   ├── research/
│   │   │   ├── portfolio/
│   │   │   └── alerts/
│   │   ├── utils/            # Utilities
│   │   └── main.py           # FastAPI app
│   ├── tests/
│   ├── alembic/              # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js app directory
│   │   ├── components/       # React components
│   │   ├── lib/              # Utilities
│   │   ├── hooks/            # Custom hooks
│   │   └── types/            # TypeScript types
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── data/                     # Data storage
├── docs/                     # Documentation
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your environment
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local  # Configure your environment
npm run dev
```

### Docker Setup
```bash
docker-compose up -d
```

## 📊 Database Schema

### Core Tables
- `companies` - Master company data
- `stock_prices` - Time series price data
- `financial_statements` - Income, Balance Sheet, Cash Flow
- `ratios` - Calculated financial metrics
- `news` - Aggregated news articles
- `earnings_calls` - Transcript storage
- `analyst_estimates` - Consensus estimates
- `watchlists` - User watchlists
- `research_notes` - User research documentation
- `screener_results` - Cached screening results
- `dcf_models` - Valuation models
- `portfolios` - User portfolio holdings
- `alerts` - User alert configurations

## 🔧 Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/stockanalysis
REDIS_URL=redis://localhost:6379/0

# API Keys (if needed for premium features)
# Most features use free sources

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

## 📖 API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 📈 Key Features Explained

### Stock Screener
Filter stocks using 50+ criteria including:
- Valuation metrics (P/E, P/B, EV/EBITDA)
- Profitability (ROE, ROA, ROIC)
- Growth (Revenue, Earnings, FCF)
- Financial health (Debt/Equity, Current Ratio)
- Efficiency (Asset Turnover, Inventory Turnover)

### Financial Analysis
- 10+ years historical data
- Common-size statements
- 40+ calculated ratios
- Peer comparison
- Trend analysis (CAGR)
- Red flag detection

### DCF Valuation
- Customizable assumptions
- 5-10 year projections
- WACC calculation
- Terminal value estimation
- Sensitivity analysis
- Fair value estimates

### Portfolio Tracking
- XIRR/IRR calculations
- Performance attribution
- Dividend tracking
- Risk metrics (Sharpe, Beta, Alpha)
- Benchmark comparison

## 🤝 Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Richard Coffin's 6-step fundamental analysis framework
- NSE/BSE for data availability
- Open-source Python finance community

## 📞 Support

For issues and questions, please open a GitHub issue.

---

**Disclaimer**: This platform is for educational and research purposes only. Always consult with qualified financial advisors before making investment decisions.
