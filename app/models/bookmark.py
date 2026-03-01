from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Bookmark(Base):
    """User bookmarked/saved questions for later review."""
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="bookmarks")
    question = relationship("Question")

    # Ensure user can't bookmark same question twice
    __table_args__ = (
        UniqueConstraint('user_id', 'question_id', name='unique_user_question_bookmark'),
    )

    def __repr__(self):
        return f"<Bookmark(id={self.id}, user_id={self.user_id}, question_id={self.question_id})>"
