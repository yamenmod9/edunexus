from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookmarkCreate(BaseModel):
    """Schema for creating a bookmark."""
    question_id: int


class BookmarkResponse(BaseModel):
    """Schema for bookmark response."""
    id: int
    user_id: int
    question_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BookmarkWithQuestion(BaseModel):
    """Schema for bookmark with question details."""
    id: int
    question_id: int
    created_at: datetime
    # Question details will be included via join
    question_text: Optional[str] = None
    section: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None

    class Config:
        from_attributes = True
