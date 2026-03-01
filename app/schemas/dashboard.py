from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List, Dict


class DashboardStatsResponse(BaseModel):
    """Complete dashboard statistics response."""
    # Today's stats
    questions_solved_today: int
    correct_today: int
    incorrect_today: int
    time_spent_today: float  # minutes

    # Overall stats
    total_questions_solved: int
    total_correct: int
    total_incorrect: int
    overall_accuracy: float  # percentage

    # Section-specific
    math_accuracy: float
    english_accuracy: float
    math_total: int
    english_total: int

    # Bookmarks and tests
    bookmarked_count: int
    tests_completed: int

    # SAT exam countdown
    sat_exam_date: Optional[date]
    days_until_exam: Optional[int]
    target_score: Optional[int]

    # Recent performance (last 7 days)
    recent_accuracy: float
    recent_questions_count: int


class PerformanceGraphData(BaseModel):
    """Time-series data for performance graphs."""
    date: date
    questions_attempted: int
    accuracy: float
    math_accuracy: Optional[float]
    english_accuracy: Optional[float]


class PerformanceGraphResponse(BaseModel):
    """Response containing graph data."""
    daily_performance: List[PerformanceGraphData]
    period_days: int  # 7, 30, or 90


class SectionPerformance(BaseModel):
    """Section-specific performance breakdown."""
    section: str
    total_questions: int
    correct: int
    incorrect: int
    accuracy: float
    avg_time_per_question: float  # seconds


class CategoryPerformance(BaseModel):
    """Category-specific performance for English."""
    category: str
    subcategory: Optional[str]
    total_questions: int
    correct: int
    accuracy: float
    difficulty_breakdown: Dict[str, float]  # {easy: 0.9, medium: 0.7, hard: 0.5}


class ErrorLogEntry(BaseModel):
    """Single mistake entry."""
    question_id: int
    question_text: str
    section: str
    category: Optional[str]
    subcategory: Optional[str]
    difficulty: str
    user_answer: str
    correct_answer: str
    attempted_at: datetime
    source_type: str  # 'practice' or 'test'
    reviewed: bool


class ErrorLogResponse(BaseModel):
    """Grouped error logs by date."""
    date: date
    mistakes: List[ErrorLogEntry]
    total_mistakes: int


class ScorePredictionResponse(BaseModel):
    """Score prediction details."""
    predicted_total_score: int  # 400-1600
    predicted_math_score: int  # 200-800
    predicted_english_score: int  # 200-800
    confidence_level: float  # 0.0 to 1.0
    sample_size: int
    easy_accuracy: Optional[float]
    medium_accuracy: Optional[float]
    hard_accuracy: Optional[float]
    created_at: datetime
    calculation_method: str

    # Additional insights
    strengths: List[str]  # Categories where user performs well
    weaknesses: List[str]  # Categories needing improvement
    recommended_study_areas: List[str]

    class Config:
        from_attributes = True


class DailyStatisticResponse(BaseModel):
    """Daily statistic details."""
    date: date
    questions_attempted: int
    questions_correct: int
    questions_incorrect: int
    math_attempted: int
    math_correct: int
    english_attempted: int
    english_correct: int
    total_time_spent: float
    tests_completed: int
    accuracy: float

    class Config:
        from_attributes = True
