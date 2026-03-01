from flask import Blueprint, request, jsonify, g
from datetime import datetime
import random
from app.api.utils import get_db_session, login_required
from app.models import User, Test, TestAttempt, Question

tests_bp = Blueprint('tests', __name__, url_prefix='/api/tests')


@tests_bp.route('/generate', methods=['POST'])
@login_required
def generate_test():
    """Generate a new test for the user."""
    data = request.get_json()
    if not data or not data.get("test_type"):
        return jsonify({"detail": "test_type is required"}), 400

    db = get_db_session()
    current_user = g.current_user

    num_questions = data.get("num_questions", 50)

    # Get random questions from database
    questions = db.query(Question).order_by(Question.id).limit(num_questions * 2).all()

    if len(questions) < num_questions:
        return jsonify({"detail": "Not enough questions available"}), 400

    # Randomly select questions
    selected_questions = random.sample(questions, min(num_questions, len(questions)))
    question_ids = [q.id for q in selected_questions]

    # Create test
    test = Test(
        user_id=current_user.id,
        test_type=data["test_type"],
        questions=question_ids,
    )

    db.add(test)
    db.commit()
    db.refresh(test)

    # Create empty test attempts
    for question_id in question_ids:
        test_attempt = TestAttempt(
            test_id=test.id,
            question_id=question_id,
        )
        db.add(test_attempt)

    db.commit()

    return jsonify({
        "id": test.id,
        "user_id": test.user_id,
        "test_type": test.test_type,
        "questions": test.questions,
        "started_at": test.started_at.isoformat() if test.started_at else None,
        "submitted_at": test.submitted_at.isoformat() if test.submitted_at else None,
        "score": test.score,
    }), 200


@tests_bp.route('/submit', methods=['POST'])
@login_required
def submit_test():
    """Submit a completed test."""
    data = request.get_json()
    if not data or not data.get("test_id") or not data.get("answers"):
        return jsonify({"detail": "test_id and answers are required"}), 400

    db = get_db_session()
    current_user = g.current_user

    # Verify test belongs to user
    test = db.query(Test).filter(
        Test.id == data["test_id"],
        Test.user_id == current_user.id
    ).first()

    if not test:
        return jsonify({"detail": "Test not found"}), 404

    if test.submitted_at:
        return jsonify({"detail": "Test already submitted"}), 400

    # Process answers
    correct_count = 0
    total_count = len(data["answers"])

    for answer_data in data["answers"]:
        question_id = answer_data.get("question_id")
        user_answer = answer_data.get("user_answer", "").upper()

        # Get question
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            continue

        is_correct = user_answer == question.correct_answer.value
        if is_correct:
            correct_count += 1

        # Update test attempt
        test_attempt = db.query(TestAttempt).filter(
            TestAttempt.test_id == test.id,
            TestAttempt.question_id == question_id
        ).first()

        if test_attempt:
            test_attempt.user_answer = user_answer
            test_attempt.is_correct = is_correct
            test_attempt.answered_at = datetime.utcnow()

    # Calculate score (percentage)
    score = (correct_count / total_count * 100) if total_count > 0 else 0.0

    # Update test
    test.submitted_at = datetime.utcnow()
    test.score = score

    db.commit()

    return jsonify({
        "test_id": test.id,
        "score": score,
        "total_questions": total_count,
        "correct_answers": correct_count,
        "submitted_at": test.submitted_at.isoformat(),
    }), 200


@tests_bp.route('/history', methods=['GET'])
@login_required
def get_test_history():
    """Get test history for the current user."""
    db = get_db_session()
    current_user = g.current_user

    tests = db.query(Test).filter(
        Test.user_id == current_user.id
    ).order_by(
        Test.started_at.desc()
    ).all()

    history = []
    for test in tests:
        history.append({
            "test_id": test.id,
            "test_type": test.test_type,
            "started_at": test.started_at.isoformat() if test.started_at else None,
            "submitted_at": test.submitted_at.isoformat() if test.submitted_at else None,
            "score": test.score,
            "total_questions": len(test.questions) if test.questions else 0,
        })

    return jsonify(history), 200
