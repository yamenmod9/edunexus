from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # SAT exam tracking
    sat_exam_date = Column(Date, nullable=True, index=True)
    target_score = Column(Integer, nullable=True)  # Target total score (400-1600)

    # Relationships
    practice_sessions = relationship("PracticeSession", back_populates="user")
    tests = relationship("Test", back_populates="user")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    daily_statistics = relationship("DailyStatistic", back_populates="user", cascade="all, delete-orphan")
    mistake_logs = relationship("MistakeLog", back_populates="user", cascade="all, delete-orphan")
    score_predictions = relationship("ScorePrediction", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
