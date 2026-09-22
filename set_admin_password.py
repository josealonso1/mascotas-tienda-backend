"""Set (or create) the admin password without storing it in any file.

Run from the project root with the venv active:
    python set_admin_password.py
"""
import os
import sys
from getpass import getpass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Admin
from app.auth import get_password_hash

MIN_LENGTH = 12
MAX_BYTES = 72  # bcrypt ignores anything beyond 72 bytes


def main():
    username = input("Admin username [admin]: ").strip() or "admin"
    password = getpass("New password: ")
    confirm = getpass("Repeat password: ")

    if password != confirm:
        print("Passwords do not match. Nothing was changed.")
        return
    if len(password) < MIN_LENGTH:
        print(f"Password must have at least {MIN_LENGTH} characters. Nothing was changed.")
        return
    if len(password.encode("utf-8")) > MAX_BYTES:
        print(f"Password must be at most {MAX_BYTES} bytes long. Nothing was changed.")
        return

    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == username).first()
        hashed = get_password_hash(password)
        if admin:
            admin.hashed_password = hashed
            action = "updated"
        else:
            db.add(Admin(username=username, hashed_password=hashed))
            action = "created"
        db.commit()
        print(f"Admin '{username}' {action}.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()