"""
Digital SAT Score Calculation Model (Bluebook-Based)

Updated for NEW Digital SAT structure with adaptive modules
"""
from sqlalchemy import Column, Integer, Float, DateTime, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class ScoreCalculation(Base):
    """
    Stores Digital SAT score calculations made by users.

    Digital SAT Structure (Bluebook):
    - Reading & Writing: 27q Module 1 + 27q Module 2 (adaptive)
    - Math: 22q Module 1 + 22q Module 2 (adaptive)
    """
    __tablename__ = "score_calculations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Reading & Writing Module scores
    rw_module1_correct = Column(Integer, nullable=False, comment="R&W Module 1 correct (0-27)")
    rw_module2_correct = Column(Integer, nullable=False, comment="R&W Module 2 correct (0-27)")
    rw_module2_difficulty = Column(
        String(10),
        nullable=False,
        comment="R&W Module 2 difficulty: easy/medium/hard"
    )

    # Math Module scores
    math_module1_correct = Column(Integer, nullable=False, comment="Math Module 1 correct (0-22)")
    math_module2_correct = Column(Integer, nullable=False, comment="Math Module 2 correct (0-22)")
    math_module2_difficulty = Column(
        String(10),
        nullable=False,
        comment="Math Module 2 difficulty: easy/medium/hard"
    )

    # Calculated section scores
    reading_writing_score = Column(Integer, nullable=False, comment="R&W section score (200-800)")
    math_score = Column(Integer, nullable=False, comment="Math section score (200-800)")
    total_score = Column(Integer, nullable=False, index=True, comment="Total score (400-1600)")

    # Percentile and confidence
    percentile = Column(Integer, comment="Estimated percentile (1-99)")
    confidence = Column(String(10), comment="Confidence level: low/medium/high")

    # Estimation metadata
    is_estimated = Column(Boolean, default=True, nullable=False, comment="Always True for Digital SAT estimates")

    # Metadata
    calculation_date = Column(DateTime, default=datetime.utcnow, index=True)
    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="score_calculations")

    def __repr__(self):
        return (
            f"<ScoreCalculation(id={self.id}, user_id={self.user_id}, "
            f"total={self.total_score}, RW={self.reading_writing_score}, "
            f"Math={self.math_score})>"
        )

    @property
    def rw_total_correct(self) -> int:
        """Total correct answers in R&W (Module 1 + Module 2)"""
        return self.rw_module1_correct + self.rw_module2_correct

    @property
    def math_total_correct(self) -> int:
        """Total correct answers in Math (Module 1 + Module 2)"""
        return self.math_module1_correct + self.math_module2_correct

    @property
    def rw_accuracy(self) -> float:
        """Reading & Writing accuracy percentage"""
        return (self.rw_total_correct / 54) * 100  # 54 total R&W questions

    @property
    def math_accuracy(self) -> float:
        """Math accuracy percentage"""
        return (self.math_total_correct / 44) * 100  # 44 total Math questions

    @property
    def overall_accuracy(self) -> float:
        """Overall accuracy percentage"""
        total_correct = self.rw_total_correct + self.math_total_correct
        return (total_correct / 98) * 100  # 98 total questions

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            # Module inputs
            'rw_module1_correct': self.rw_module1_correct,
            'rw_module2_correct': self.rw_module2_correct,
            'rw_module2_difficulty': self.rw_module2_difficulty,
            'math_module1_correct': self.math_module1_correct,
            'math_module2_correct': self.math_module2_correct,
            'math_module2_difficulty': self.math_module2_difficulty,
            # Calculated scores
            'reading_writing_score': self.reading_writing_score,
            'math_score': self.math_score,
            'total_score': self.total_score,
            'percentile': self.percentile,
            'confidence': self.confidence,
            # Metadata
            'is_estimated': self.is_estimated,
            'calculation_date': self.calculation_date.isoformat() if self.calculation_date else None,
            'notes': self.notes,
            # Computed properties
            'rw_total_correct': self.rw_total_correct,
            'math_total_correct': self.math_total_correct,
            'rw_accuracy': round(self.rw_accuracy, 2),
            'math_accuracy': round(self.math_accuracy, 2),
            'overall_accuracy': round(self.overall_accuracy, 2)
        }
