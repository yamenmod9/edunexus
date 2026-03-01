from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from app.models.question import SectionEnum, DifficultyEnum, CorrectAnswerEnum


class QuestionBase(BaseModel):
    section: SectionEnum
    topic: str = Field(..., min_length=1, max_length=100)
    subtopic: Optional[str] = Field(None, max_length=100)

    # New SAT hierarchy fields
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)

    difficulty: DifficultyEnum
    question_text: str = Field(..., min_length=1)
    choices: List[str] = Field(..., min_length=4, max_length=4)
    correct_answer: CorrectAnswerEnum
    explanation: Optional[str] = None

    # Bluebook flag
    is_bluebook: bool = False

    # Additional metadata
    passage_text: Optional[str] = None
    source_attribution: Optional[str] = Field(None, max_length=200)

    @field_validator('choices')
    @classmethod
    def validate_choices(cls, v):
        if len(v) != 4:
            raise ValueError('Must have exactly 4 choices')
        if any(not choice.strip() for choice in v):
            raise ValueError('All choices must be non-empty')
        return v


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionResponseWithoutAnswer(BaseModel):
    """Question response without correct answer and explanation (for tests)."""
    id: int
    section: SectionEnum
    topic: str
    subtopic: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    difficulty: DifficultyEnum
    question_text: str
    choices: List[str]
    is_bluebook: bool
    passage_text: Optional[str]
    source_attribution: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
