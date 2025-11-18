#!/usr/bin/env python3
"""
Quick script to create an admin user
Usage: python create_admin.py
"""
from app.core.database import SessionLocal
from app.models import User
from passlib.context import CryptContext
import sys

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_admin():
    """Create admin user interactively"""
    print("\n" + "="*50)
    print("Create Admin User")
    print("="*50 + "\n")

    # Get input
    email = input("Email: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    full_name = input("Full Name (optional): ").strip()

    if not email or not username or not password:
        print("\n❌ Email, username, and password are required!")
        sys.exit(1)

    # Create user
    db = SessionLocal()
    try:
        # Check if user exists
        existing = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing:
            print(f"\n❌ User with email '{email}' or username '{username}' already exists!")
            sys.exit(1)

        # Create admin
        admin = User(
            email=email,
            username=username,
            hashed_password=pwd_context.hash(password),
            full_name=full_name or None,
            is_active=True,
            is_superuser=True
        )

        db.add(admin)
        db.commit()

        print("\n" + "="*50)
        print("✓ Admin user created successfully!")
        print("="*50)
        print(f"\nEmail: {email}")
        print(f"Username: {username}")
        print(f"Superuser: Yes")
        print("\nYou can now login with these credentials.\n")

    except Exception as e:
        print(f"\n❌ Error creating admin: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
