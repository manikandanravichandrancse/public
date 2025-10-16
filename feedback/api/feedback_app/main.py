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
def get_all_feedback(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[schemas.FeedbackResponse]:
    """
    Retrieve all feedback entries with pagination.

    Args:
        skip (int): Number of records to skip (default: 0).
        limit (int): Maximum number of records to return (default: 100, max: 1000).
        db (Session): Database session provided by dependency.

    Returns:
        List[FeedbackResponse]: List of feedback entries.

    Raises:
        HTTPException: If database operation fails.
    """
    try:
        # Limit validation
        if limit > settings.max_page_size:
            limit = settings.max_page_size

        feedbacks = db.query(models.Feedback).offset(skip).limit(limit).all()
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


@app.get(
    "/api/latest/feedback/{feedback_id}",
    response_model=schemas.FeedbackResponse,
    summary="Get feedback by ID",
    description="Retrieve a specific feedback entry by its ID",
    tags=["Feedback"],
)
def get_feedback(
    feedback_id: int, db: Session = Depends(get_db)
) -> schemas.FeedbackResponse:
    """
    Retrieve a specific feedback entry by ID.

    Args:
        feedback_id (int): The ID of the feedback to retrieve.
        db (Session): Database session provided by dependency.

    Returns:
        FeedbackResponse: The requested feedback entry.

    Raises:
        HTTPException: If feedback not found or database error occurs.
    """
    try:
        feedback = (
            db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
        )

        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback with ID {feedback_id} not found",
            )

        return feedback
    except HTTPException:
        raise
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


@app.delete(
    "/api/latest/feedback/{feedback_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete feedback",
    description="Delete a specific feedback entry by its ID",
    tags=["Feedback"],
)
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a specific feedback entry by ID.

    Args:
        feedback_id (int): The ID of the feedback to delete.
        db (Session): Database session provided by dependency.

    Raises:
        HTTPException: If feedback not found or database error occurs.
    """
    try:
        feedback = (
            db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
        )

        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback with ID {feedback_id} not found",
            )

        db.delete(feedback)
        db.commit()
    except HTTPException:
        raise
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
    "/api/latest/health",
    summary="Health check",
    description="Check if the API is running",
    tags=["Health"],
)
def health_check():
    """
    Health check endpoint.

    Returns:
        dict: API status information.
    """
    return {
        "status": "healthy",
        "service": settings.api_title,
        "version": settings.api_version,
    }
