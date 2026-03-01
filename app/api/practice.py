from flask import Blueprint, request, jsonify, g
from sqlalchemy import func
from datetime import datetime
from app.api.utils import get_db_session, login_required
from app.models import User, PracticeSession, Attempt, Question
from app.services.analytics import AnalyticsService

practice_bp = Blueprint('practice', __name__, url_prefix='/api/practice')


def attempt_to_dict(a):
    """Serialize an Attempt model to a dict."""
    return {
        "id": a.id,
        "session_id": a.session_id,
        "question_id": a.question_id,
        "user_answer": a.user_answer,
        "is_correct": a.is_correct,
        "time_spent": a.time_spent,
        "attempted_at": a.attempted_at.isoformat() if a.attempted_at else None,
    }


def session_to_dict(s):
    """Serialize a PracticeSession model to a dict."""
    return {
        "id": s.id,
        "user_id": s.user_id,
        "topics": s.topics,
        "started_at": s.started_at.isoformat() if s.started_at else None,
        "ended_at": s.ended_at.isoformat() if s.ended_at else None,
    }


@practice_bp.route('/session/start', methods=['POST'])
@login_required
def start_practice_session():
    """Start a new practice session."""
    data = request.get_json()
    if not data or not data.get("topics"):
        return jsonify({"detail": "Topics are required"}), 400

    db = get_db_session()
    current_user = g.current_user

    session = PracticeSession(
        user_id=current_user.id,
        topics=",".join(data["topics"]),
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return jsonify(session_to_dict(session)), 200


@practice_bp.route('/attempt', methods=['POST'])
@login_required
def submit_attempt():
    """Submit an attempt for a question in a practice session."""
    data = request.get_json()
    if not data:
        return jsonify({"detail": "Request body is required"}), 400

    session_id = data.get("session_id")
    question_id = data.get("question_id")
    user_answer = data.get("user_answer", "")
    time_spent = data.get("time_spent")

    if not session_id or not question_id or not user_answer:
        return jsonify({"detail": "session_id, question_id, and user_answer are required"}), 400

    db = get_db_session()
    current_user = g.current_user

    # Verify session belongs to user
    session = db.query(PracticeSession).filter(
        PracticeSession.id == session_id,
        PracticeSession.user_id == current_user.id
    ).first()

    if not session:
        return jsonify({"detail": "Practice session not found"}), 404

    # Get question
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return jsonify({"detail": "Question not found"}), 404

    # Check if answer is correct
    is_correct = user_answer.upper() == question.correct_answer.value

    # Create attempt
    attempt = Attempt(
        session_id=session_id,
        question_id=question_id,
        user_answer=user_answer.upper(),
        is_correct=is_correct,
        time_spent=time_spent,
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # Log mistake if answer is incorrect
    if not is_correct:
        AnalyticsService.log_mistake(
            db=db,
            user_id=current_user.id,
            question_id=question_id,
            user_answer=user_answer.upper(),
            source_type='practice',
            source_id=session_id,
            time_spent=time_spent
        )

    # Update daily statistics
    AnalyticsService.update_daily_statistics(db, current_user.id)

    return jsonify(attempt_to_dict(attempt)), 200


@practice_bp.route('/history', methods=['GET'])
@login_required
def get_practice_history():
    """Get practice history for the current user."""
    db = get_db_session()
    current_user = g.current_user

    # Query sessions with attempt statistics
    sessions = db.query(
        PracticeSession.id.label("session_id"),
        PracticeSession.topics,
        PracticeSession.started_at,
        PracticeSession.ended_at,
        func.count(Attempt.id).label("total_attempts"),
        func.sum(func.cast(Attempt.is_correct, db.bind.dialect.name == 'sqlite' and 'INTEGER' or 'INTEGER')).label("correct_attempts"),
    ).join(
        Attempt, PracticeSession.id == Attempt.session_id, isouter=True
    ).filter(
        PracticeSession.user_id == current_user.id
    ).group_by(
        PracticeSession.id
    ).order_by(
        PracticeSession.started_at.desc()
    ).all()

    # Format results
    history = []
    for session in sessions:
        total = session.total_attempts or 0
        correct = session.correct_attempts or 0
        accuracy = (correct / total * 100) if total > 0 else 0.0

        history.append({
            "session_id": session.session_id,
            "topics": session.topics,
            "started_at": session.started_at.isoformat() if session.started_at else None,
            "ended_at": session.ended_at.isoformat() if session.ended_at else None,
            "total_attempts": total,
            "correct_attempts": correct,
            "accuracy": accuracy,
        })

    return jsonify(history), 200
