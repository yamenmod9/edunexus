from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    test_type = Column(String(50), nullable=False)  # e.g., "full_sat", "math_only"
    questions = Column(JSON, nullable=False)  # Array of question IDs
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    submitted_at = Column(DateTime, nullable=True)
    score = Column(Float, nullable=True)

    # Relationships
    user = relationship("User", back_populates="tests")
    test_attempts = relationship("TestAttempt", back_populates="test")

    def __repr__(self):
        return f"<Test(id={self.id}, user_id={self.user_id}, test_type={self.test_type})>"


class TestAttempt(Base):
    __tablename__ = "test_attempts"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    user_answer = Column(String(1), nullable=True)  # Nullable for unanswered
    is_correct = Column(Boolean, nullable=True)
    time_spent = Column(Float, nullable=True)  # seconds
    answered_at = Column(DateTime, nullable=True)

    # Relationships
    test = relationship("Test", back_populates="test_attempts")
    question = relationship("Question")

    def __repr__(self):
        return f"<TestAttempt(id={self.id}, test_id={self.test_id}, question_id={self.question_id})>"
