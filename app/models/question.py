from sqlalchemy import Column, Integer, String, Text, Enum as SQLEnum, DateTime, Index, Boolean
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
import enum
from app.db.base import Base


class SectionEnum(str, enum.Enum):
    MATH = "math"
    ENGLISH = "english"  # Combined reading/writing for SAT structure


class DifficultyEnum(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class CorrectAnswerEnum(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


# SAT English Categories
class EnglishCategoryEnum(str, enum.Enum):
    CRAFT_AND_STRUCTURE = "craft_and_structure"
    EXPRESSION_OF_IDEAS = "expression_of_ideas"
    INFORMATION_AND_IDEAS = "information_and_ideas"
    STANDARD_ENGLISH_CONVENTIONS = "standard_english_conventions"


# SAT English Subcategories
class EnglishSubcategoryEnum(str, enum.Enum):
    # Craft and Structure
    CROSS_TEXT_CONNECTIONS = "cross_text_connections"
    TEXT_STRUCTURE_AND_PURPOSE = "text_structure_and_purpose"
    WORDS_IN_CONTEXT = "words_in_context"

    # Expression of Ideas
    RHETORICAL_SYNTHESIS = "rhetorical_synthesis"
    TRANSITIONS = "transitions"

    # Information and Ideas
    CENTRAL_IDEAS_AND_DETAILS = "central_ideas_and_details"
    COMMAND_OF_EVIDENCE = "command_of_evidence"
    INFERENCES = "inferences"

    # Standard English Conventions
    BOUNDARIES = "boundaries"
    FORM_STRUCTURE_AND_SENSE = "form_structure_and_sense"


# Math Categories (for future use)
class MathCategoryEnum(str, enum.Enum):
    ALGEBRA = "algebra"
    ADVANCED_MATH = "advanced_math"
    PROBLEM_SOLVING_DATA_ANALYSIS = "problem_solving_data_analysis"
    GEOMETRY_TRIGONOMETRY = "geometry_trigonometry"


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    section = Column(SQLEnum(SectionEnum), nullable=False, index=True)

    # Legacy fields (kept for backward compatibility)
    topic = Column(String(100), nullable=True, index=True)
    subtopic = Column(String(100), nullable=True)

    # New SAT-accurate hierarchy
    category = Column(String(100), nullable=True, index=True)  # Main category
    subcategory = Column(String(100), nullable=True, index=True)  # Specific subcategory

    difficulty = Column(SQLEnum(DifficultyEnum), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    choices = Column(JSON, nullable=False)  # Array of 4 strings
    correct_answer = Column(SQLEnum(CorrectAnswerEnum), nullable=False)
    explanation = Column(Text, nullable=True)

    # Bluebook flag (digital SAT indicator)
    is_bluebook = Column(Boolean, default=False, nullable=False, index=True)

    # Additional metadata
    passage_text = Column(Text, nullable=True)  # For reading comprehension questions
    source_attribution = Column(String(200), nullable=True)  # Author, work, etc.

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Composite indexes for common queries
    __table_args__ = (
        Index('idx_section_difficulty', 'section', 'difficulty'),
        Index('idx_section_category', 'section', 'category'),
        Index('idx_section_subcategory', 'section', 'subcategory'),
        Index('idx_category_subcategory', 'category', 'subcategory'),
        Index('idx_section_bluebook', 'section', 'is_bluebook'),
    )

    def __repr__(self):
        return f"<Question(id={self.id}, section={self.section}, category={self.category}, subcategory={self.subcategory})>"
