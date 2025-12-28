"""Database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Get database session for dependency injection.

    Yields:
        Database session

    Raises:
        Exception: Any database-related errors are handled by FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
