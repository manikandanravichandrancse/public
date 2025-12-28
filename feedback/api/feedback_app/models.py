"""
SQLAlchemy ORM models for the feedback application.

Defines the Feedback model representing feedback entries
in the SQLite database with proper indexing and constraints.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base


class Feedback(Base):
    """
    Feedback model representing a feedback entry.

    Attributes:
        id (int): Primary key of the feedback entry.
        name (str | None): Name of the person giving feedback.
        email (str | None): Email of the person giving feedback.
        message (str): Feedback message (required).
        rating (int | None): Rating given (optional, 1-5).
        created_at (datetime): Timestamp when the feedback was created.
        updated_at (datetime): Timestamp when the feedback was last updated.
    """
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True, index=True)
    mobile = Column(String(13), nullable=True)
    message = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        """String representation of Feedback instance."""
        return f"<Feedback(id={self.id}, name={self.name}, rating={self.rating})>"
