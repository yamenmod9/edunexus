from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class TestGenerate(BaseModel):
    test_type: str = Field(..., min_length=1, max_length=50)
    num_questions: Optional[int] = Field(None, ge=1, le=200)


class TestResponse(BaseModel):
    id: int
    user_id: int
    test_type: str
    questions: List[int]
    started_at: datetime
    submitted_at: Optional[datetime]
    score: Optional[float]

    class Config:
        from_attributes = True


class TestSubmit(BaseModel):
    test_id: int
    answers: List[dict]  # [{question_id: int, user_answer: str}]


class TestSubmitResponse(BaseModel):
    test_id: int
    score: float
    total_questions: int
    correct_answers: int
    submitted_at: datetime


class TestHistoryResponse(BaseModel):
    test_id: int
    test_type: str
    started_at: datetime
    submitted_at: Optional[datetime]
    score: Optional[float]
    total_questions: int
