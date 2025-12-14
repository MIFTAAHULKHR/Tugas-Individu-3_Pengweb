# create_tables.py
import sys
import os

# Tambahkan current directory ke path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base
from models import Review

def create_tables():
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    create_tables()