"""Score prediction service using weighted accuracy and SAT scoring curves."""
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime
from typing import List, Dict, Tuple
from app.models import (
    User, Question, Attempt, PracticeSession, Test, TestAttempt, ScorePrediction
)


class ScorePredictionService:
    """Service for predicting SAT scores based on practice performance."""

    # SAT score conversion table (simplified - actual SAT uses complex curves)
    # Maps percentage correct to scaled score (200-800)
    SCORE_CURVE = {
        100: 800, 95: 760, 90: 720, 85: 680, 80: 640,
        75: 600, 70: 560, 65: 520, 60: 480, 55: 440,
        50: 400, 45: 360, 40: 320, 35: 280, 30: 240, 0: 200
    }

    # Minimum sample sizes for reliable predictions
    MIN_SAMPLE_MATH = 30
    MIN_SAMPLE_ENGLISH = 40

    @staticmethod
    def calculate_score_prediction(db: Session, user_id: int) -> Dict:
        """Calculate comprehensive score prediction for a user."""

        # Get all attempts (practice + tests)
        math_attempts = ScorePredictionService._get_section_attempts(db, user_id, 'math')
        english_attempts = ScorePredictionService._get_section_attempts(db, user_id, 'english')

        # Calculate weighted accuracy by difficulty
        math_accuracy, math_sample = ScorePredictionService._calculate_weighted_accuracy(math_attempts)
        english_accuracy, english_sample = ScorePredictionService._calculate_weighted_accuracy(english_attempts)

        # Determine confidence level based on sample size
        math_confidence = min(math_sample / ScorePredictionService.MIN_SAMPLE_MATH, 1.0)
        english_confidence = min(english_sample / ScorePredictionService.MIN_SAMPLE_ENGLISH, 1.0)
        overall_confidence = (math_confidence + english_confidence) / 2

        # Convert accuracy to SAT scores
        math_score = ScorePredictionService._accuracy_to_score(math_accuracy)
        english_score = ScorePredictionService._accuracy_to_score(english_accuracy)
        total_score = math_score + english_score

        # Get difficulty breakdown
        difficulty_breakdown = ScorePredictionService._get_difficulty_breakdown(
            math_attempts + english_attempts
        )

        # Identify strengths and weaknesses
        strengths, weaknesses = ScorePredictionService._identify_strengths_weaknesses(
            db, user_id
        )

        # Generate recommendations
        recommendations = ScorePredictionService._generate_recommendations(
            math_accuracy, english_accuracy, weaknesses
        )

        # Save prediction
        prediction = ScorePrediction(
            user_id=user_id,
            predicted_total_score=total_score,
            predicted_math_score=math_score,
            predicted_english_score=english_score,
            confidence_level=overall_confidence,
            sample_size=math_sample + english_sample,
            easy_accuracy=difficulty_breakdown.get('easy'),
            medium_accuracy=difficulty_breakdown.get('medium'),
            hard_accuracy=difficulty_breakdown.get('hard'),
            calculation_method='weighted_accuracy',
            created_at=datetime.utcnow()
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        return {
            "predicted_total_score": total_score,
            "predicted_math_score": math_score,
            "predicted_english_score": english_score,
            "confidence_level": overall_confidence,
            "sample_size": math_sample + english_sample,
            "easy_accuracy": difficulty_breakdown.get('easy'),
            "medium_accuracy": difficulty_breakdown.get('medium'),
            "hard_accuracy": difficulty_breakdown.get('hard'),
            "created_at": prediction.created_at,
            "calculation_method": 'weighted_accuracy',
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommended_study_areas": recommendations,
        }

    @staticmethod
    def _get_section_attempts(db: Session, user_id: int, section: str) -> List[Tuple]:
        """Get all attempts for a specific section."""
        # Practice attempts
        practice = db.query(
            Question.difficulty,
            Attempt.is_correct
        ).join(
            Attempt, Attempt.question_id == Question.id
        ).join(
            PracticeSession, PracticeSession.id == Attempt.session_id
        ).filter(
            PracticeSession.user_id == user_id,
            Question.section == section
        ).all()

        # Test attempts
        test = db.query(
            Question.difficulty,
            TestAttempt.is_correct
        ).join(
            TestAttempt, TestAttempt.question_id == Question.id
        ).join(
            Test, Test.id == TestAttempt.test_id
        ).filter(
            Test.user_id == user_id,
            Question.section == section,
            TestAttempt.is_correct.isnot(None)  # Only count answered questions
        ).all()

        return practice + test

    @staticmethod
    def _calculate_weighted_accuracy(attempts: List[Tuple]) -> Tuple[float, int]:
        """
        Calculate weighted accuracy giving more importance to harder questions.

        Weights: Easy=1.0, Medium=1.5, Hard=2.0
        """
        if not attempts:
            return 0.0, 0

        weights = {'easy': 1.0, 'medium': 1.5, 'hard': 2.0}
        total_weight = 0.0
        weighted_correct = 0.0

        for difficulty, is_correct in attempts:
            weight = weights.get(difficulty.value, 1.0)
            total_weight += weight
            if is_correct:
                weighted_correct += weight

        weighted_accuracy = (weighted_correct / total_weight * 100) if total_weight > 0 else 0.0
        return weighted_accuracy, len(attempts)

    @staticmethod
    def _accuracy_to_score(accuracy: float) -> int:
        """Convert accuracy percentage to SAT score using curve."""
        # Find the closest score in the curve
        for threshold in sorted(ScorePredictionService.SCORE_CURVE.keys(), reverse=True):
            if accuracy >= threshold:
                return ScorePredictionService.SCORE_CURVE[threshold]
        return 200  # Minimum score

    @staticmethod
    def _get_difficulty_breakdown(attempts: List[Tuple]) -> Dict[str, float]:
        """Get accuracy breakdown by difficulty level."""
        by_difficulty = {'easy': {'total': 0, 'correct': 0},
                        'medium': {'total': 0, 'correct': 0},
                        'hard': {'total': 0, 'correct': 0}}

        for difficulty, is_correct in attempts:
            diff_key = difficulty.value
            by_difficulty[diff_key]['total'] += 1
            if is_correct:
                by_difficulty[diff_key]['correct'] += 1

        result = {}
        for diff, data in by_difficulty.items():
            if data['total'] > 0:
                result[diff] = data['correct'] / data['total']

        return result

    @staticmethod
    def _identify_strengths_weaknesses(db: Session, user_id: int) -> Tuple[List[str], List[str]]:
        """Identify user's strengths and weaknesses by category."""
        # Get category performance for English
        category_stats = db.query(
            Question.category,
            func.count(Attempt.id).label('total'),
            func.sum(case((Attempt.is_correct == True, 1), else_=0)).label('correct')
        ).join(
            Attempt, Attempt.question_id == Question.id
        ).join(
            PracticeSession, PracticeSession.id == Attempt.session_id
        ).filter(
            PracticeSession.user_id == user_id,
            Question.category.isnot(None)
        ).group_by(Question.category).all()

        # Also get from tests
        test_category_stats = db.query(
            Question.category,
            func.count(TestAttempt.id).label('total'),
            func.sum(case((TestAttempt.is_correct == True, 1), else_=0)).label('correct')
        ).join(
            TestAttempt, TestAttempt.question_id == Question.id
        ).join(
            Test, Test.id == TestAttempt.test_id
        ).filter(
            Test.user_id == user_id,
            Question.category.isnot(None)
        ).group_by(Question.category).all()

        # Combine and calculate accuracy
        combined = {}
        for category, total, correct in category_stats:
            combined[category] = {'total': total or 0, 'correct': correct or 0}

        for category, total, correct in test_category_stats:
            if category in combined:
                combined[category]['total'] += total or 0
                combined[category]['correct'] += correct or 0
            else:
                combined[category] = {'total': total or 0, 'correct': correct or 0}

        # Calculate accuracy and identify strengths/weaknesses
        strengths = []
        weaknesses = []

        for category, data in combined.items():
            if data['total'] >= 5:  # Only consider categories with enough data
                accuracy = data['correct'] / data['total']
                readable_name = category.replace('_', ' ').title()

                if accuracy >= 0.8:
                    strengths.append(readable_name)
                elif accuracy < 0.6:
                    weaknesses.append(readable_name)

        return strengths, weaknesses

    @staticmethod
    def _generate_recommendations(math_accuracy: float, english_accuracy: float,
                                 weaknesses: List[str]) -> List[str]:
        """Generate study recommendations based on performance."""
        recommendations = []

        # Overall recommendations
        if math_accuracy < 60:
            recommendations.append("Focus on Math fundamentals - consider reviewing Algebra and Problem-Solving")
        elif math_accuracy < 75:
            recommendations.append("Practice more challenging Math problems to improve score")

        if english_accuracy < 60:
            recommendations.append("Build English foundation - focus on grammar rules and reading comprehension")
        elif english_accuracy < 75:
            recommendations.append("Work on advanced English concepts and timed practice")

        # Specific category recommendations
        if weaknesses:
            recommendations.append(f"Priority areas to improve: {', '.join(weaknesses[:3])}")

        # General advice
        if math_accuracy > 75 and english_accuracy > 75:
            recommendations.append("Strong performance! Focus on full-length practice tests and time management")

        if not recommendations:
            recommendations.append("Continue practicing across all sections to maintain performance")

        return recommendations

    @staticmethod
    def get_latest_prediction(db: Session, user_id: int) -> Dict:
        """Get the most recent score prediction for a user."""
        prediction = db.query(ScorePrediction).filter(
            ScorePrediction.user_id == user_id
        ).order_by(ScorePrediction.created_at.desc()).first()

        if not prediction:
            return None

        # Get fresh strengths/weaknesses
        strengths, weaknesses = ScorePredictionService._identify_strengths_weaknesses(db, user_id)
        recommendations = ScorePredictionService._generate_recommendations(
            prediction.predicted_math_score / 800 * 100,
            prediction.predicted_english_score / 800 * 100,
            weaknesses
        )

        return {
            "predicted_total_score": prediction.predicted_total_score,
            "predicted_math_score": prediction.predicted_math_score,
            "predicted_english_score": prediction.predicted_english_score,
            "confidence_level": prediction.confidence_level,
            "sample_size": prediction.sample_size,
            "easy_accuracy": prediction.easy_accuracy,
            "medium_accuracy": prediction.medium_accuracy,
            "hard_accuracy": prediction.hard_accuracy,
            "created_at": prediction.created_at,
            "calculation_method": prediction.calculation_method,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommended_study_areas": recommendations,
        }
