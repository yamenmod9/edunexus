"""Bookmark API endpoints for saving questions."""
from flask import Blueprint, request, jsonify, g
from sqlalchemy.exc import IntegrityError
from app.api.utils import get_db_session, login_required
from app.models import Bookmark, Question

bookmarks_bp = Blueprint('bookmarks', __name__, url_prefix='/api/bookmarks')


@bookmarks_bp.route('/', methods=['POST'])
@login_required
def create_bookmark():
    """Bookmark a question for later review."""
    data = request.get_json()
    if not data or not data.get("question_id"):
        return jsonify({"detail": "question_id is required"}), 400

    db = get_db_session()

    # Check if question exists
    question = db.query(Question).filter(Question.id == data["question_id"]).first()
    if not question:
        return jsonify({"detail": "Question not found"}), 404

    # Create bookmark
    bookmark = Bookmark(
        user_id=g.current_user.id,
        question_id=data["question_id"]
    )

    try:
        db.add(bookmark)
        db.commit()
        db.refresh(bookmark)
    except IntegrityError:
        db.rollback()
        return jsonify({"detail": "Question already bookmarked"}), 400

    return jsonify({
        "id": bookmark.id,
        "user_id": bookmark.user_id,
        "question_id": bookmark.question_id,
        "created_at": bookmark.created_at.isoformat() if bookmark.created_at else None,
    }), 201


@bookmarks_bp.route('/', methods=['GET'])
@login_required
def get_bookmarks():
    """Get all bookmarked questions for the current user."""
    db = get_db_session()

    bookmarks = db.query(
        Bookmark.id,
        Bookmark.question_id,
        Bookmark.created_at,
        Question.question_text,
        Question.section,
        Question.category,
        Question.difficulty
    ).join(
        Question, Question.id == Bookmark.question_id
    ).filter(
        Bookmark.user_id == g.current_user.id
    ).order_by(
        Bookmark.created_at.desc()
    ).all()

    result = []
    for b in bookmarks:
        result.append({
            "id": b.id,
            "question_id": b.question_id,
            "created_at": b.created_at.isoformat() if b.created_at else None,
            "question_text": b.question_text,
            "section": b.section.value if b.section else None,
            "category": b.category,
            "difficulty": b.difficulty.value if b.difficulty else None,
        })

    return jsonify(result), 200


@bookmarks_bp.route('/<int:bookmark_id>', methods=['DELETE'])
@login_required
def delete_bookmark(bookmark_id):
    """Remove a bookmark."""
    db = get_db_session()

    bookmark = db.query(Bookmark).filter(
        Bookmark.id == bookmark_id,
        Bookmark.user_id == g.current_user.id
    ).first()

    if not bookmark:
        return jsonify({"detail": "Bookmark not found"}), 404

    db.delete(bookmark)
    db.commit()

    return '', 204


@bookmarks_bp.route('/question/<int:question_id>', methods=['DELETE'])
@login_required
def delete_bookmark_by_question(question_id):
    """Remove a bookmark by question ID."""
    db = get_db_session()

    bookmark = db.query(Bookmark).filter(
        Bookmark.question_id == question_id,
        Bookmark.user_id == g.current_user.id
    ).first()

    if not bookmark:
        return jsonify({"detail": "Bookmark not found"}), 404

    db.delete(bookmark)
    db.commit()

    return '', 204


@bookmarks_bp.route('/check/<int:question_id>', methods=['GET'])
@login_required
def check_bookmark_status(question_id):
    """Check if a question is bookmarked."""
    db = get_db_session()

    bookmark = db.query(Bookmark).filter(
        Bookmark.question_id == question_id,
        Bookmark.user_id == g.current_user.id
    ).first()

    return jsonify({
        "is_bookmarked": bookmark is not None,
        "bookmark_id": bookmark.id if bookmark else None,
    }), 200
