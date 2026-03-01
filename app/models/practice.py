from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topics = Column(String, nullable=False)  # Comma-separated list
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="practice_sessions")
    attempts = relationship("Attempt", back_populates="session")

    def __repr__(self):
        return f"<PracticeSession(id={self.id}, user_id={self.user_id})>"


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("practice_sessions.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    user_answer = Column(String(1), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_spent = Column(Float, nullable=True)  # seconds
    attempted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    session = relationship("PracticeSession", back_populates="attempts")
    question = relationship("Question")

    def __repr__(self):
        return f"<Attempt(id={self.id}, question_id={self.question_id}, is_correct={self.is_correct})>"
