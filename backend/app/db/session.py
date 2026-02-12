# backend/app/db/session.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Check environment variables first (Docker-friendly), then try .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# If not in environment, try loading from .env file
if not DATABASE_URL:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    dotenv_path = os.path.join(PROJECT_ROOT, ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set. Please set it as an environment variable "
        "or in a .env file in the project root."
    )

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
