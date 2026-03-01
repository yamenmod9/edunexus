from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List


class MistakeQuestion(BaseModel):
    id: int
    question_text: str
    question_type: str
    difficulty: str
    subject: str
    topic: str
    correct_answer: str
    explanation: Optional[str] = None

    class Config:
        from_attributes = True


class MistakeResponse(BaseModel):
    id: int
    question: MistakeQuestion
    user_answer: str
    answered_at: datetime
    time_spent: Optional[int] = None

    class Config:
        from_attributes = True


class CommonTopic(BaseModel):
    topic: str
    count: int


class MistakeStatsResponse(BaseModel):
    total_mistakes: int
    mistakes_by_subject: Dict[str, int]
    mistakes_by_difficulty: Dict[str, int]
    common_topics: List[CommonTopic]

    class Config:
        from_attributes = True
