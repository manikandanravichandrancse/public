"""
FastAPI app for managing feedback.

This module provides endpoints to create and retrieve feedback
from a SQLite database using SQLAlchemy ORM with production-ready
error handling, validation, and best practices.
"""

from typing import Any, Generator, List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from . import models, schemas
from .database import SessionLocal, engine
from .config import settings

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> Generator[Session, Any, None]:
    """
    Dependency to get a database session.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/api/latest/feedback",
    response_model=schemas.FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new feedback",
    description="Submit new feedback with optional name, email, and rating",
    tags=["Feedback"],
)
def create_feedback(
    feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)
) -> schemas.FeedbackResponse:
    """
    Create a new feedback entry in the database.

    Args:
        feedback (FeedbackCreate): Feedback data from the request body.
        db (Session): Database session provided by dependency.

    Returns:
        FeedbackResponse: The created feedback entry with ID.

    Raises:
        HTTPException: If database operation fails.
    """
    try:
        new_feedback = models.Feedback(**feedback.model_dump())
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        return new_feedback
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@app.get(
    "/api/latest/feedback",
    response_model=List[schemas.FeedbackResponse],
    summary="Get all feedback",
    description="Retrieve all feedback entries from the database with pagination",
    tags=["Feedback"],
)
def get_all_feedback(db: Session = Depends(get_db)) -> List[schemas.FeedbackResponse]:
    """
    Retrieve all feedback entries with pagination.

    Args:
        limit (int): Maximum number of records to return (default: 100, max: 1000).
        db (Session): Database session provided by dependency.

    Returns:
        List[FeedbackResponse]: List of feedback entries.

    Raises:
        HTTPException: If database operation fails.
    """
    try:
        feedbacks = db.query(models.Feedback).all()
        return feedbacks
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )
