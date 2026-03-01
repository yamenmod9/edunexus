"""Analytics service for computing dashboard statistics and predictions."""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, case
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from app.models import (
    User, Question, Attempt, PracticeSession, Test, TestAttempt,
    DailyStatistic, MistakeLog, ScorePrediction, Bookmark, SectionEnum
)


class AnalyticsService:
    """Service for computing analytics and dashboard statistics."""

    @staticmethod
    def get_dashboard_stats(db: Session, user_id: int) -> Dict:
        """Get comprehensive dashboard statistics for a user."""
        today = date.today()

        # Get or create today's statistics
        today_stats = db.query(DailyStatistic).filter(
            DailyStatistic.user_id == user_id,
            DailyStatistic.date == today
        ).first()

        # Overall statistics from all attempts
        practice_stats = db.query(
            func.count(Attempt.id).label('total'),
            func.sum(case((Attempt.is_correct == True, 1), else_=0)).label('correct'),
        ).join(PracticeSession).filter(
            PracticeSession.user_id == user_id
        ).first()

        test_stats = db.query(
            func.count(TestAttempt.id).label('total'),
            func.sum(case((TestAttempt.is_correct == True, 1), else_=0)).label('correct'),
        ).join(Test).filter(
            Test.user_id == user_id
        ).first()

        total_questions = (practice_stats.total or 0) + (test_stats.total or 0)
        total_correct = (practice_stats.correct or 0) + (test_stats.correct or 0)

        # Section-specific statistics
        section_stats = AnalyticsService._get_section_statistics(db, user_id)

        # Bookmarks count
        bookmarks_count = db.query(func.count(Bookmark.id)).filter(
            Bookmark.user_id == user_id
        ).scalar() or 0

        # Tests completed
        tests_completed = db.query(func.count(Test.id)).filter(
            Test.user_id == user_id,
            Test.submitted_at.isnot(None)
        ).scalar() or 0

        # User's SAT exam info
        user = db.query(User).filter(User.id == user_id).first()
        days_until_exam = None
        if user and user.sat_exam_date:
            days_until_exam = (user.sat_exam_date - today).days

        # Recent performance (last 7 days)
        seven_days_ago = today - timedelta(days=7)
        recent_stats = db.query(
            func.sum(DailyStatistic.questions_attempted).label('total'),
            func.sum(DailyStatistic.questions_correct).label('correct')
        ).filter(
            DailyStatistic.user_id == user_id,
            DailyStatistic.date >= seven_days_ago
        ).first()

        recent_total = recent_stats.total or 0
        recent_correct = recent_stats.correct or 0
        recent_accuracy = (recent_correct / recent_total * 100) if recent_total > 0 else 0.0

        return {
            "questions_solved_today": today_stats.questions_attempted if today_stats else 0,
            "correct_today": today_stats.questions_correct if today_stats else 0,
            "incorrect_today": today_stats.questions_incorrect if today_stats else 0,
            "time_spent_today": (today_stats.total_time_spent / 60) if today_stats else 0.0,  # Convert to minutes
            "total_questions_solved": total_questions,
            "total_correct": total_correct,
            "total_incorrect": total_questions - total_correct,
            "overall_accuracy": (total_correct / total_questions * 100) if total_questions > 0 else 0.0,
            "math_accuracy": section_stats.get('math', {}).get('accuracy', 0.0),
            "english_accuracy": section_stats.get('english', {}).get('accuracy', 0.0),
            "math_total": section_stats.get('math', {}).get('total', 0),
            "english_total": section_stats.get('english', {}).get('total', 0),
            "bookmarked_count": bookmarks_count,
            "tests_completed": tests_completed,
            "sat_exam_date": user.sat_exam_date if user else None,
            "days_until_exam": days_until_exam,
            "target_score": user.target_score if user else None,
            "recent_accuracy": recent_accuracy,
            "recent_questions_count": recent_total,
        }

    @staticmethod
    def _get_section_statistics(db: Session, user_id: int) -> Dict:
        """Get statistics broken down by section."""
        stats = {}

        # Practice attempts by section
        practice_by_section = db.query(
            Question.section,
            func.count(Attempt.id).label('total'),
            func.sum(case((Attempt.is_correct == True, 1), else_=0)).label('correct')
        ).join(Attempt, Attempt.question_id == Question.id
        ).join(PracticeSession, PracticeSession.id == Attempt.session_id
        ).filter(
            PracticeSession.user_id == user_id
        ).group_by(Question.section).all()

        # Test attempts by section
        test_by_section = db.query(
            Question.section,
            func.count(TestAttempt.id).label('total'),
            func.sum(case((TestAttempt.is_correct == True, 1), else_=0)).label('correct')
        ).join(TestAttempt, TestAttempt.question_id == Question.id
        ).join(Test, Test.id == TestAttempt.test_id
        ).filter(
            Test.user_id == user_id
        ).group_by(Question.section).all()

        # Combine practice and test stats
        combined = {}
        for section, total, correct in practice_by_section:
            combined[section.value] = {'total': total or 0, 'correct': correct or 0}

        for section, total, correct in test_by_section:
            section_key = section.value
            if section_key in combined:
                combined[section_key]['total'] += total or 0
                combined[section_key]['correct'] += correct or 0
            else:
                combined[section_key] = {'total': total or 0, 'correct': correct or 0}

        # Calculate accuracy
        for section_key, data in combined.items():
            total = data['total']
            correct = data['correct']
            data['accuracy'] = (correct / total * 100) if total > 0 else 0.0

        return combined

    @staticmethod
    def get_performance_graph_data(db: Session, user_id: int, days: int = 7) -> List[Dict]:
        """Get time-series performance data for graphs."""
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)

        daily_stats = db.query(DailyStatistic).filter(
            DailyStatistic.user_id == user_id,
            DailyStatistic.date >= start_date,
            DailyStatistic.date <= end_date
        ).order_by(DailyStatistic.date).all()

        result = []
        for stat in daily_stats:
            accuracy = (stat.questions_correct / stat.questions_attempted * 100) if stat.questions_attempted > 0 else 0.0
            math_accuracy = (stat.math_correct / stat.math_attempted * 100) if stat.math_attempted > 0 else None
            english_accuracy = (stat.english_correct / stat.english_attempted * 100) if stat.english_attempted > 0 else None

            result.append({
                "date": stat.date,
                "questions_attempted": stat.questions_attempted,
                "accuracy": accuracy,
                "math_accuracy": math_accuracy,
                "english_accuracy": english_accuracy,
            })

        return result

    @staticmethod
    def get_error_logs(db: Session, user_id: int, days: int = 30, limit: int = 100) -> List[Dict]:
        """Get mistake logs grouped by date."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        mistakes = db.query(
            MistakeLog,
            Question
        ).join(
            Question, Question.id == MistakeLog.question_id
        ).filter(
            MistakeLog.user_id == user_id,
            MistakeLog.attempted_at >= cutoff_date
        ).order_by(
            MistakeLog.attempted_at.desc()
        ).limit(limit).all()

        # Group by date
        grouped = {}
        for mistake, question in mistakes:
            mistake_date = mistake.attempted_at.date()
            if mistake_date not in grouped:
                grouped[mistake_date] = []

            grouped[mistake_date].append({
                "question_id": question.id,
                "question_text": question.question_text[:200] + "..." if len(question.question_text) > 200 else question.question_text,
                "section": question.section.value,
                "category": question.category,
                "subcategory": question.subcategory,
                "difficulty": question.difficulty.value,
                "user_answer": mistake.user_answer,
                "correct_answer": question.correct_answer.value,
                "attempted_at": mistake.attempted_at,
                "source_type": mistake.source_type,
                "reviewed": mistake.reviewed,
            })

        # Convert to list format
        result = []
        for mistake_date, mistakes_list in sorted(grouped.items(), reverse=True):
            result.append({
                "date": mistake_date,
                "mistakes": mistakes_list,
                "total_mistakes": len(mistakes_list),
            })

        return result

    @staticmethod
    def get_category_performance(db: Session, user_id: int, section: str) -> List[Dict]:
        """Get performance breakdown by category and subcategory."""
        # Combine practice and test attempts
        practice_attempts = db.query(
            Question.category,
            Question.subcategory,
            Question.difficulty,
            Attempt.is_correct
        ).join(
            Attempt, Attempt.question_id == Question.id
        ).join(
            PracticeSession, PracticeSession.id == Attempt.session_id
        ).filter(
            PracticeSession.user_id == user_id,
            Question.section == section,
            Question.category.isnot(None)
        ).all()

        test_attempts = db.query(
            Question.category,
            Question.subcategory,
            Question.difficulty,
            TestAttempt.is_correct
        ).join(
            TestAttempt, TestAttempt.question_id == Question.id
        ).join(
            Test, Test.id == TestAttempt.test_id
        ).filter(
            Test.user_id == user_id,
            Question.section == section,
            Question.category.isnot(None)
        ).all()

        # Combine and aggregate
        stats = {}
        for category, subcategory, difficulty, is_correct in practice_attempts + test_attempts:
            key = (category, subcategory or "general")
            if key not in stats:
                stats[key] = {
                    'total': 0,
                    'correct': 0,
                    'difficulties': {'easy': {'total': 0, 'correct': 0},
                                    'medium': {'total': 0, 'correct': 0},
                                    'hard': {'total': 0, 'correct': 0}}
                }

            stats[key]['total'] += 1
            if is_correct:
                stats[key]['correct'] += 1

            diff_key = difficulty.value if difficulty else 'medium'
            stats[key]['difficulties'][diff_key]['total'] += 1
            if is_correct:
                stats[key]['difficulties'][diff_key]['correct'] += 1

        # Format results
        result = []
        for (category, subcategory), data in stats.items():
            difficulty_breakdown = {}
            for diff, diff_data in data['difficulties'].items():
                if diff_data['total'] > 0:
                    difficulty_breakdown[diff] = diff_data['correct'] / diff_data['total']

            result.append({
                "category": category,
                "subcategory": subcategory if subcategory != "general" else None,
                "total_questions": data['total'],
                "correct": data['correct'],
                "accuracy": (data['correct'] / data['total'] * 100) if data['total'] > 0 else 0.0,
                "difficulty_breakdown": difficulty_breakdown,
            })

        return sorted(result, key=lambda x: x['total_questions'], reverse=True)

    @staticmethod
    def update_daily_statistics(db: Session, user_id: int, date_to_update: date = None):
        """Update or create daily statistics for a user."""
        if date_to_update is None:
            date_to_update = date.today()

        # Get or create daily statistic
        daily_stat = db.query(DailyStatistic).filter(
            DailyStatistic.user_id == user_id,
            DailyStatistic.date == date_to_update
        ).first()

        if not daily_stat:
            daily_stat = DailyStatistic(user_id=user_id, date=date_to_update)
            db.add(daily_stat)

        # Calculate statistics for the day
        start_datetime = datetime.combine(date_to_update, datetime.min.time())
        end_datetime = datetime.combine(date_to_update, datetime.max.time())

        # Practice attempts
        practice_attempts = db.query(
            func.count(Attempt.id).label('total'),
            func.sum(case((Attempt.is_correct == True, 1), else_=0)).label('correct'),
            func.sum(Attempt.time_spent).label('time_spent')
        ).join(PracticeSession).filter(
            PracticeSession.user_id == user_id,
            Attempt.attempted_at >= start_datetime,
            Attempt.attempted_at <= end_datetime
        ).first()

        # Test attempts
        test_attempts = db.query(
            func.count(TestAttempt.id).label('total'),
            func.sum(case((TestAttempt.is_correct == True, 1), else_=0)).label('correct'),
            func.sum(TestAttempt.time_spent).label('time_spent')
        ).join(Test).filter(
            Test.user_id == user_id,
            TestAttempt.answered_at >= start_datetime,
            TestAttempt.answered_at <= end_datetime
        ).first()

        total_attempted = (practice_attempts.total or 0) + (test_attempts.total or 0)
        total_correct = (practice_attempts.correct or 0) + (test_attempts.correct or 0)
        total_time = (practice_attempts.time_spent or 0) + (test_attempts.time_spent or 0)

        # Section-specific stats
        section_stats = AnalyticsService._get_daily_section_stats(db, user_id, start_datetime, end_datetime)

        # Tests completed
        tests_completed = db.query(func.count(Test.id)).filter(
            Test.user_id == user_id,
            Test.submitted_at >= start_datetime,
            Test.submitted_at <= end_datetime
        ).scalar() or 0

        # Update the record
        daily_stat.questions_attempted = total_attempted
        daily_stat.questions_correct = total_correct
        daily_stat.questions_incorrect = total_attempted - total_correct
        daily_stat.math_attempted = section_stats.get('math', {}).get('total', 0)
        daily_stat.math_correct = section_stats.get('math', {}).get('correct', 0)
        daily_stat.english_attempted = section_stats.get('english', {}).get('total', 0)
        daily_stat.english_correct = section_stats.get('english', {}).get('correct', 0)
        daily_stat.total_time_spent = total_time
        daily_stat.tests_completed = tests_completed
        daily_stat.updated_at = datetime.utcnow()

        db.commit()
        return daily_stat

    @staticmethod
    def _get_daily_section_stats(db: Session, user_id: int, start_datetime: datetime, end_datetime: datetime) -> Dict:
        """Get section statistics for a specific day."""
        stats = {}

        # Practice by section
        practice_by_section = db.query(
            Question.section,
            func.count(Attempt.id).label('total'),
            func.sum(case((Attempt.is_correct == True, 1), else_=0)).label('correct')
        ).join(Attempt, Attempt.question_id == Question.id
        ).join(PracticeSession, PracticeSession.id == Attempt.session_id
        ).filter(
            PracticeSession.user_id == user_id,
            Attempt.attempted_at >= start_datetime,
            Attempt.attempted_at <= end_datetime
        ).group_by(Question.section).all()

        # Test by section
        test_by_section = db.query(
            Question.section,
            func.count(TestAttempt.id).label('total'),
            func.sum(case((TestAttempt.is_correct == True, 1), else_=0)).label('correct')
        ).join(TestAttempt, TestAttempt.question_id == Question.id
        ).join(Test, Test.id == TestAttempt.test_id
        ).filter(
            Test.user_id == user_id,
            TestAttempt.answered_at >= start_datetime,
            TestAttempt.answered_at <= end_datetime
        ).group_by(Question.section).all()

        # Combine
        for section, total, correct in practice_by_section:
            stats[section.value] = {'total': total or 0, 'correct': correct or 0}

        for section, total, correct in test_by_section:
            section_key = section.value
            if section_key in stats:
                stats[section_key]['total'] += total or 0
                stats[section_key]['correct'] += correct or 0
            else:
                stats[section_key] = {'total': total or 0, 'correct': correct or 0}

        return stats

    @staticmethod
    def log_mistake(db: Session, user_id: int, question_id: int, user_answer: str,
                   source_type: str, source_id: int, time_spent: float = None):
        """Log a mistake for later review."""
        mistake = MistakeLog(
            user_id=user_id,
            question_id=question_id,
            user_answer=user_answer,
            source_type=source_type,
            source_id=source_id,
            time_spent=time_spent,
            attempted_at=datetime.utcnow()
        )
        db.add(mistake)
        db.commit()
        return mistake
