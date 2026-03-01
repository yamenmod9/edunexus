from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Date, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class DailyStatistic(Base):
    """Daily aggregated statistics for user performance."""
    __tablename__ = "daily_statistics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)

    # Daily counts
    questions_attempted = Column(Integer, default=0, nullable=False)
    questions_correct = Column(Integer, default=0, nullable=False)
    questions_incorrect = Column(Integer, default=0, nullable=False)

    # Section-specific counts
    math_attempted = Column(Integer, default=0, nullable=False)
    math_correct = Column(Integer, default=0, nullable=False)
    english_attempted = Column(Integer, default=0, nullable=False)
    english_correct = Column(Integer, default=0, nullable=False)

    # Time tracking
    total_time_spent = Column(Float, default=0.0, nullable=False)  # seconds

    # Tests
    tests_completed = Column(Integer, default=0, nullable=False)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="daily_statistics")

    # Ensure one record per user per day
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'date', unique=True),
    )

    def __repr__(self):
        return f"<DailyStatistic(user_id={self.user_id}, date={self.date}, questions_attempted={self.questions_attempted})>"


class MistakeLog(Base):
    """Tracks incorrect answers for mistake review feature."""
    __tablename__ = "mistake_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)

    # Attempt details
    user_answer = Column(String(1), nullable=False)
    attempted_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Source of mistake (practice session or test)
    source_type = Column(String(20), nullable=False)  # 'practice' or 'test'
    source_id = Column(Integer, nullable=False)  # session_id or test_id

    # Review tracking
    reviewed = Column(Boolean, default=False, nullable=False)
    reviewed_at = Column(DateTime, nullable=True)

    time_spent = Column(Float, nullable=True)  # seconds

    # Relationships
    user = relationship("User", back_populates="mistake_logs")
    question = relationship("Question")

    __table_args__ = (
        Index('idx_user_attempted_at', 'user_id', 'attempted_at'),
        Index('idx_user_reviewed', 'user_id', 'reviewed'),
    )

    def __repr__(self):
        return f"<MistakeLog(id={self.id}, user_id={self.user_id}, question_id={self.question_id}, attempted_at={self.attempted_at})>"


class ScorePrediction(Base):
    """Stores score predictions based on practice performance."""
    __tablename__ = "score_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Prediction results
    predicted_total_score = Column(Integer, nullable=False)  # 400-1600
    predicted_math_score = Column(Integer, nullable=False)   # 200-800
    predicted_english_score = Column(Integer, nullable=False) # 200-800

    # Confidence metrics
    confidence_level = Column(Float, nullable=False)  # 0.0 to 1.0
    sample_size = Column(Integer, nullable=False)  # Number of questions used for prediction

    # Breakdown by difficulty
    easy_accuracy = Column(Float, nullable=True)
    medium_accuracy = Column(Float, nullable=True)
    hard_accuracy = Column(Float, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    calculation_method = Column(String(50), nullable=False)  # e.g., 'weighted_accuracy', 'linear_regression'

    # Relationships
    user = relationship("User", back_populates="score_predictions")

    def __repr__(self):
        return f"<ScorePrediction(user_id={self.user_id}, predicted_total={self.predicted_total_score}, confidence={self.confidence_level})>"
