"""
Pydantic schemas for the feedback application.

Defines data validation and serialization models for
creating and retrieving feedback entries with Pydantic v2 support.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class FeedbackBase(BaseModel):
    """
    Base schema for feedback with validation.

    Attributes:
        name (str | None): Name of the person giving feedback. Optional, max 50 chars.
        email (EmailStr | None): Email of the person giving feedback. Optional.
        message (str): Feedback message (required, 10-500 chars).
        rating (int | None): Rating given (optional, 1-5).
    """
    name: Optional[str] = Field(None, max_length=50, description="Name of the person")
    email: Optional[EmailStr] = Field(None, description="Email address")
    mobile: Optional[str] = Field(None, max_length=13, description="Mobile number of the person")
    message: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Feedback message"
    )
    rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Rating from 1 to 5"
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from name if provided."""
        if v is not None:
            return v.strip()
        return v

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Strip whitespace and validate message."""
        stripped = v.strip()
        if len(stripped) < 10:
            raise ValueError('Message must be at least 10 characters after stripping whitespace')
        return stripped


class FeedbackCreate(FeedbackBase):
    """
    Schema for creating new feedback.

    Inherits all fields from FeedbackBase.
    Used for POST requests to create feedback.
    """
    pass


class FeedbackResponse(FeedbackBase):
    """
    Schema for returning feedback to clients.

    Attributes:
        id (int): Unique identifier for the feedback entry.
        created_at (datetime | None): Timestamp when feedback was created.
    """
    id: int = Field(..., description="Unique feedback ID")

    model_config = {
        "from_attributes": True,  # Pydantic v2 replacement for orm_mode
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "mobile": "+919999999999",
                "message": "Great service! Really enjoyed the experience.",
                "rating": 5
            }
        }
    }
