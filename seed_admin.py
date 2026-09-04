"""
Seed script to create the initial admin user.
Run this script after setting up the database to create the admin account.
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Admin
from app.auth import get_password_hash
from app.config import settings

def create_admin_user():
    """Create admin user if it doesn't already exist"""
    db: Session = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(Admin).filter(Admin.username == settings.ADMIN_USERNAME).first()
        
        if existing_admin:
            print(f"Admin user '{settings.ADMIN_USERNAME}' already exists. Skipping creation.")
            return
        
        # Hash the password
        hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
        
        # Create new admin
        new_admin = Admin(
            username=settings.ADMIN_USERNAME,
            hashed_password=hashed_password
        )
        
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        
        print(f"Admin user '{settings.ADMIN_USERNAME}' created successfully!")
        print("Please change the password after first login for security.")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating admin user: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created or already exist.")
    
    # Create admin user
    print("Creating admin user...")
    create_admin_user()
