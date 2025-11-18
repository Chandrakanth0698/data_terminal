"""
Database seeding script - Create initial admin user and sample data
"""
from datetime import datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.database import SessionLocal, engine
from app.models import User, Company
from app.core.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def create_admin_user(db: Session):
    """Create default admin user"""
    admin = db.query(User).filter(User.username == "admin").first()

    if admin:
        print("✓ Admin user already exists")
        return

    admin = User(
        email="admin@stockanalysis.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),  # Change this!
        full_name="System Administrator",
        is_active=True,
        is_superuser=True
    )

    db.add(admin)
    db.commit()
    print("✓ Admin user created")
    print("  Email: admin@stockanalysis.com")
    print("  Username: admin")
    print("  Password: admin123")
    print("  ⚠️  Please change the password after first login!")


def create_sample_companies(db: Session):
    """Create sample companies for testing"""
    sample_companies = [
        {
            "symbol": "RELIANCE",
            "name": "Reliance Industries Limited",
            "isin": "INE002A01018",
            "exchange": "NSE",
            "sector": "Oil & Gas",
            "industry": "Refineries",
            "description": "Reliance Industries Limited is an Indian multinational conglomerate, headquartered in Mumbai. It has diverse businesses including energy, petrochemicals, natural gas, retail, telecommunications, mass media, and textiles.",
            "website": "https://www.ril.com",
            "headquarters": "Mumbai, India",
            "market_cap": 1700000.0,  # in Crores
        },
        {
            "symbol": "TCS",
            "name": "Tata Consultancy Services Limited",
            "isin": "INE467B01029",
            "exchange": "NSE",
            "sector": "Information Technology",
            "industry": "IT Services & Consulting",
            "description": "Tata Consultancy Services is an Indian multinational information technology services and consulting company headquartered in Mumbai.",
            "website": "https://www.tcs.com",
            "headquarters": "Mumbai, India",
            "market_cap": 1300000.0,
        },
        {
            "symbol": "HDFCBANK",
            "name": "HDFC Bank Limited",
            "isin": "INE040A01034",
            "exchange": "NSE",
            "sector": "Financial Services",
            "industry": "Private Sector Bank",
            "description": "HDFC Bank Limited is an Indian banking and financial services company headquartered in Mumbai.",
            "website": "https://www.hdfcbank.com",
            "headquarters": "Mumbai, India",
            "market_cap": 1200000.0,
        },
        {
            "symbol": "INFY",
            "name": "Infosys Limited",
            "isin": "INE009A01021",
            "exchange": "NSE",
            "sector": "Information Technology",
            "industry": "IT Services & Consulting",
            "description": "Infosys Limited is an Indian multinational information technology company that provides business consulting, information technology and outsourcing services.",
            "website": "https://www.infosys.com",
            "headquarters": "Bengaluru, India",
            "market_cap": 700000.0,
        },
        {
            "symbol": "ICICIBANK",
            "name": "ICICI Bank Limited",
            "isin": "INE090A01021",
            "exchange": "NSE",
            "sector": "Financial Services",
            "industry": "Private Sector Bank",
            "description": "ICICI Bank Limited is an Indian multinational bank and financial services company headquartered in Mumbai.",
            "website": "https://www.icicibank.com",
            "headquarters": "Mumbai, India",
            "market_cap": 700000.0,
        },
    ]

    existing_count = db.query(Company).count()
    if existing_count > 0:
        print(f"✓ {existing_count} companies already exist in database")
        return

    for company_data in sample_companies:
        company = Company(**company_data, is_active=1)
        db.add(company)

    db.commit()
    print(f"✓ Created {len(sample_companies)} sample companies")


def init_database():
    """Initialize database with tables and seed data"""
    print("\n" + "="*50)
    print("Database Initialization")
    print("="*50 + "\n")

    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ All tables created\n")

    # Create session
    db = SessionLocal()

    try:
        # Create admin user
        print("Creating admin user...")
        create_admin_user(db)
        print()

        # Create sample companies
        print("Creating sample companies...")
        create_sample_companies(db)
        print()

        print("="*50)
        print("Database initialization completed!")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
