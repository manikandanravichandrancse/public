"""
Database setup for the feedback application.

This module creates the SQLAlchemy engine, session, and base
class for defining ORM models with production-ready configuration.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
from .config import settings


# Database configuration
DATABASE_URL = settings.database_url

# Create database engine with optimized settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 30,  # 30 seconds timeout for SQLite
        },
        pool_pre_ping=True,  # Verify connections before using
        echo=False,  # Set to True for SQL query logging in development
    )

    # Enable foreign key constraints for SQLite
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")  # Better concurrency
        cursor.close()

else:
    # For PostgreSQL/MySQL in production
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False,
    )

# SessionLocal will be used in routes to interact with the DB
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

# Base class for models
Base = declarative_base()


def get_db_session():
    """
    Create a new database session.

    This function can be used outside of FastAPI dependency injection.

    Returns:
        Session: SQLAlchemy database session
    """
    return SessionLocal()
