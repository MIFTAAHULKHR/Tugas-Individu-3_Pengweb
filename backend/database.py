from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ambil DATABASE_URL dari environment variable
# Default ke SQLite jika tidak ada
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./reviews.db')

print(f"Connecting to database: {DATABASE_URL}")

# Buat engine
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        echo=True  # Tampilkan SQL queries di console (opsional)
    )
else:
    engine = create_engine(DATABASE_URL, echo=True)

# Buat session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base untuk models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()