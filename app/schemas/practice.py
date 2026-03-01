from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PracticeSessionStart(BaseModel):
    topics: List[str] = Field(..., min_length=1)


class PracticeSessionResponse(BaseModel):
    id: int
    user_id: int
    topics: str
    started_at: datetime
    ended_at: Optional[datetime]

    class Config:
        from_attributes = True


class AttemptCreate(BaseModel):
    session_id: int
    question_id: int
    user_answer: str = Field(..., min_length=1, max_length=1)
    time_spent: Optional[float] = Field(None, ge=0)


class AttemptResponse(BaseModel):
    id: int
    session_id: int
    question_id: int
    user_answer: str
    is_correct: bool
    time_spent: Optional[float]
    attempted_at: datetime

    class Config:
        from_attributes = True


class PracticeHistoryResponse(BaseModel):
    session_id: int
    topics: str
    started_at: datetime
    ended_at: Optional[datetime]
    total_attempts: int
    correct_attempts: int
    accuracy: float
