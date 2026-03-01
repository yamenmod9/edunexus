"""
Digital SAT Score Calculator Schemas (Bluebook-Based)

Updated for NEW Digital SAT structure:
- Reading & Writing: 27q Module 1 + 27q Module 2 (adaptive)
- Math: 22q Module 1 + 22q Module 2 (adaptive)
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class ScoreCalculateRequest(BaseModel):
    """
    Request model for Digital SAT score calculation.

    Digital SAT Structure (Bluebook):
    - Reading & Writing Module 1: 27 questions
    - Reading & Writing Module 2: 27 questions (adaptive)
    - Math Module 1: 22 questions
    - Math Module 2: 22 questions (adaptive)
    """
    # Reading & Writing
    rw_module1_correct: int = Field(
        ...,
        ge=0,
        le=27,
        description="Number of correct answers in R&W Module 1 (0-27)"
    )
    rw_module2_correct: int = Field(
        ...,
        ge=0,
        le=27,
        description="Number of correct answers in R&W Module 2 (0-27)"
    )
    rw_module2_difficulty: Literal['easy', 'medium', 'hard'] = Field(
        ...,
        description="R&W Module 2 difficulty level (adaptive based on Module 1)"
    )

    # Math
    math_module1_correct: int = Field(
        ...,
        ge=0,
        le=22,
        description="Number of correct answers in Math Module 1 (0-22)"
    )
    math_module2_correct: int = Field(
        ...,
        ge=0,
        le=22,
        description="Number of correct answers in Math Module 2 (0-22)"
    )
    math_module2_difficulty: Literal['easy', 'medium', 'hard'] = Field(
        ...,
        description="Math Module 2 difficulty level (adaptive based on Module 1)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "rw_module1_correct": 24,
                "rw_module2_correct": 25,
                "rw_module2_difficulty": "hard",
                "math_module1_correct": 20,
                "math_module2_correct": 21,
                "math_module2_difficulty": "hard"
            }
        }


class ScoreCalculateResponse(BaseModel):
    """
    Response model for Digital SAT score calculation.

    ⚠️ IMPORTANT: These are ESTIMATED scores, not official College Board scores.
    """
    # Module input details
    rw_module1_correct: int
    rw_module2_correct: int
    rw_module2_difficulty: str
    math_module1_correct: int
    math_module2_correct: int
    math_module2_difficulty: str

    # Calculated scores
    reading_writing_score: int = Field(..., ge=200, le=800)
    math_score: int = Field(..., ge=200, le=800)
    total_score: int = Field(..., ge=400, le=1600)
    percentile: int = Field(..., ge=1, le=99)

    # Estimation metadata
    is_estimated: bool = Field(default=True, description="Always True - these are estimates")
    confidence: Literal['low', 'medium', 'high'] = Field(
        ...,
        description="Confidence in score estimate based on difficulty alignment"
    )
    disclaimer: str = Field(
        ...,
        description="Warning that scores are estimated and may vary"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "rw_module1_correct": 24,
                "rw_module2_correct": 25,
                "rw_module2_difficulty": "hard",
                "math_module1_correct": 20,
                "math_module2_correct": 21,
                "math_module2_difficulty": "hard",
                "reading_writing_score": 740,
                "math_score": 760,
                "total_score": 1500,
                "percentile": 99,
                "is_estimated": True,
                "confidence": "high",
                "disclaimer": "This is an ESTIMATED score based on a heuristic model. Actual Digital SAT scores may vary significantly. Use for practice guidance only."
            }
        }


class ScoreSaveRequest(BaseModel):
    """Request model for saving a Digital SAT score calculation."""
    # Module inputs
    rw_module1_correct: int = Field(..., ge=0, le=27)
    rw_module2_correct: int = Field(..., ge=0, le=27)
    rw_module2_difficulty: Literal['easy', 'medium', 'hard']
    math_module1_correct: int = Field(..., ge=0, le=22)
    math_module2_correct: int = Field(..., ge=0, le=22)
    math_module2_difficulty: Literal['easy', 'medium', 'hard']

    # Calculated scores
    reading_writing_score: int = Field(..., ge=200, le=800)
    math_score: int = Field(..., ge=200, le=800)
    total_score: int = Field(..., ge=400, le=1600)
    percentile: int = Field(..., ge=1, le=99)

    # Optional metadata
    confidence: Optional[Literal['low', 'medium', 'high']] = None
    notes: Optional[str] = None


class ScoreCalculationResponse(BaseModel):
    """Response model for a saved Digital SAT score calculation."""
    id: int

    # Module inputs
    rw_module1_correct: int
    rw_module2_correct: int
    rw_module2_difficulty: str
    math_module1_correct: int
    math_module2_correct: int
    math_module2_difficulty: str

    # Calculated scores
    reading_writing_score: int
    math_score: int
    total_score: int
    percentile: int

    # Metadata
    confidence: Optional[str] = None
    calculation_date: datetime
    notes: Optional[str] = None
    is_estimated: bool = Field(default=True)

    class Config:
        from_attributes = True


class ScoreStatsResponse(BaseModel):
    """Response model for Digital SAT score statistics."""
    total_calculations: int
    highest_score: Optional[int] = None
    lowest_score: Optional[int] = None
    average_score: Optional[float] = None
    latest_score: Optional[int] = None
    improvement: Optional[int] = None  # Difference from first to latest
    target_score: Optional[int] = None
    target_difference: Optional[int] = None  # Difference from target

    # Additional stats
    average_rw_score: Optional[float] = None
    average_math_score: Optional[float] = None
    consistency_score: Optional[float] = None  # Standard deviation (lower = more consistent)

    class Config:
        json_schema_extra = {
            "example": {
                "total_calculations": 5,
                "highest_score": 1520,
                "lowest_score": 1380,
                "average_score": 1450.0,
                "latest_score": 1500,
                "improvement": 120,
                "target_score": 1550,
                "target_difference": 50,
                "average_rw_score": 720.0,
                "average_math_score": 730.0,
                "consistency_score": 45.2
            }
        }
