"""Mistakes API endpoints."""
from flask import Blueprint, request, jsonify, g
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app.api.utils import get_db_session, login_required
from app.models.practice import Attempt, PracticeSession
from app.models.question import Question

mistakes_bp = Blueprint('mistakes', __name__, url_prefix='/api')


@mistakes_bp.route('/mistakes', methods=['GET'])
@login_required
def get_mistakes():
    """Get all incorrect attempts (mistakes) for the current user."""
    db = get_db_session()
    current_user = g.current_user

    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    section = request.args.get('section')
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    limit = min(int(request.args.get('limit', 100)), 500)
    skip = max(int(request.args.get('skip', 0)), 0)

    # Base query: get all incorrect attempts
    query = db.query(
        Attempt.id.label('attempt_id'),
        Attempt.attempted_at,
        Attempt.user_answer,
        Question.id.label('question_id'),
        Question.question_text,
        Question.section,
        Question.category,
        Question.subcategory,
        Question.difficulty,
        Question.correct_answer,
        Question.explanation,
        PracticeSession.id.label('session_id'),
    ).join(
        PracticeSession, Attempt.session_id == PracticeSession.id
    ).join(
        Question, Attempt.question_id == Question.id
    ).filter(
        PracticeSession.user_id == current_user.id,
        Attempt.is_correct == False
    )

    # Apply filters
    if date_from:
        query = query.filter(Attempt.attempted_at >= date_from)
    if date_to:
        end_date = datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(Attempt.attempted_at < end_date.strftime("%Y-%m-%d"))
    if section:
        query = query.filter(Question.section == section)
    if category:
        query = query.filter(Question.category == category)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)

    # Order by most recent first
    query = query.order_by(desc(Attempt.attempted_at))
    mistakes = query.offset(skip).limit(limit).all()

    # Format results
    result = []
    for m in mistakes:
        result.append({
            "attempt_id": m.attempt_id,
            "question_id": m.question_id,
            "question_text": m.question_text,
            "section": m.section.value if m.section else None,
            "category": m.category,
            "subcategory": m.subcategory,
            "difficulty": m.difficulty.value if m.difficulty else None,
            "user_answer": m.user_answer,
            "correct_answer": m.correct_answer.value if m.correct_answer else None,
            "explanation": m.explanation,
            "attempted_at": m.attempted_at.isoformat() if m.attempted_at else None,
            "session_id": m.session_id,
            "is_practice": True,
        })

    return jsonify(result), 200


@mistakes_bp.route('/mistakes/stats', methods=['GET'])
@login_required
def get_mistake_stats():
    """Get statistics about user's mistakes."""
    db = get_db_session()
    current_user = g.current_user

    # Total mistakes
    total_mistakes = db.query(Attempt).join(
        PracticeSession
    ).filter(
        PracticeSession.user_id == current_user.id,
        Attempt.is_correct == False
    ).count()

    # Mistakes this week
    week_ago = datetime.now() - timedelta(days=7)
    mistakes_this_week = db.query(Attempt).join(
        PracticeSession
    ).filter(
        PracticeSession.user_id == current_user.id,
        Attempt.is_correct == False,
        Attempt.attempted_at >= week_ago.strftime("%Y-%m-%d %H:%M:%S")
    ).count()

    # Mistakes this month
    month_ago = datetime.now() - timedelta(days=30)
    mistakes_this_month = db.query(Attempt).join(
        PracticeSession
    ).filter(
        PracticeSession.user_id == current_user.id,
        Attempt.is_correct == False,
        Attempt.attempted_at >= month_ago.strftime("%Y-%m-%d %H:%M:%S")
    ).count()

    # Mistakes by category
    by_category_raw = db.query(
        Question.category,
        func.count(Attempt.id).label('count')
    ).join(
        Attempt, Attempt.question_id == Question.id
    ).join(
        PracticeSession, Attempt.session_id == PracticeSession.id
    ).filter(
        PracticeSession.user_id == current_user.id,
        Attempt.is_correct == False,
        Question.category.isnot(None)
    ).group_by(
        Question.category
    ).order_by(
        desc('count')
    ).all()

    by_category = {cat: count for cat, count in by_category_raw}

    # Mistakes by difficulty
    by_difficulty_raw = db.query(
        Question.difficulty,
        func.count(Attempt.id).label('count')
    ).join(
        Attempt, Attempt.question_id == Question.id
    ).join(
        PracticeSession, Attempt.session_id == PracticeSession.id
    ).filter(
        PracticeSession.user_id == current_user.id,
        Attempt.is_correct == False
    ).group_by(
        Question.difficulty
    ).all()

    by_difficulty = {diff.value if hasattr(diff, 'value') else str(diff): count for diff, count in by_difficulty_raw}

    most_common_category = by_category_raw[0][0] if by_category_raw else None

    return jsonify({
        "total_mistakes": total_mistakes,
        "this_week": mistakes_this_week,
        "this_month": mistakes_this_month,
        "by_category": by_category,
        "by_difficulty": by_difficulty,
        "most_common_category": most_common_category,
    }), 200


@mistakes_bp.route('/mistakes/count', methods=['GET'])
@login_required
def get_mistakes_count():
    """Get count of mistakes with optional filters."""
    db = get_db_session()
    current_user = g.current_user

    section = request.args.get('section')
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')

    query = db.query(Attempt).join(
        PracticeSession
    ).join(
        Question, Attempt.question_id == Question.id
    ).filter(
        PracticeSession.user_id == current_user.id,
        Attempt.is_correct == False
    )

    if section:
        query = query.filter(Question.section == section)
    if category:
        query = query.filter(Question.category == category)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)

    count = query.count()

    return jsonify({"count": count}), 200
