from flask import Blueprint, request, jsonify
from app.api.utils import get_db_session
from app.models import Question, SectionEnum, DifficultyEnum, CorrectAnswerEnum
import random

questions_bp = Blueprint('questions', __name__, url_prefix='/api/questions')


def question_to_dict(q):
    """Serialize a Question model to a dict."""
    return {
        "id": q.id,
        "section": q.section.value if q.section else None,
        "topic": q.topic,
        "subtopic": q.subtopic,
        "category": q.category,
        "subcategory": q.subcategory,
        "difficulty": q.difficulty.value if q.difficulty else None,
        "question_text": q.question_text,
        "choices": q.choices,
        "correct_answer": q.correct_answer.value if q.correct_answer else None,
        "explanation": q.explanation,
        "is_bluebook": q.is_bluebook,
        "passage_text": q.passage_text,
        "source_attribution": q.source_attribution,
        "created_at": q.created_at.isoformat() if q.created_at else None,
    }


@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Get questions with optional filters."""
    db = get_db_session()

    section = request.args.get('section')
    topic = request.args.get('topic')
    subtopic = request.args.get('subtopic')
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    difficulty = request.args.get('difficulty')
    bluebook_only = request.args.get('bluebook_only', 'false').lower() == 'true'
    shuffle = request.args.get('shuffle', 'false').lower() == 'true'
    limit = min(int(request.args.get('limit', 10)), 100)
    skip = max(int(request.args.get('skip', 0)), 0)

    query = db.query(Question)

    # Apply filters
    if section:
        query = query.filter(Question.section == section)
    if topic:
        query = query.filter(Question.topic == topic)
    if subtopic:
        query = query.filter(Question.subtopic == subtopic)
    if category:
        query = query.filter(Question.category == category)
    if subcategory:
        query = query.filter(Question.subcategory == subcategory)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if bluebook_only:
        query = query.filter(Question.is_bluebook == True)

    # Get questions with pagination
    questions = query.offset(skip).limit(limit).all()

    # Shuffle if requested
    if shuffle:
        random.shuffle(questions)

    return jsonify([question_to_dict(q) for q in questions]), 200


@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Get a specific question by ID."""
    db = get_db_session()
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        return jsonify({"detail": "Question not found"}), 404

    return jsonify(question_to_dict(question)), 200


@questions_bp.route('/count/total', methods=['GET'])
def get_questions_count():
    """Get count of questions matching filters."""
    db = get_db_session()

    section = request.args.get('section')
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    difficulty = request.args.get('difficulty')
    bluebook_only = request.args.get('bluebook_only', 'false').lower() == 'true'

    query = db.query(Question)

    if section:
        query = query.filter(Question.section == section)
    if category:
        query = query.filter(Question.category == category)
    if subcategory:
        query = query.filter(Question.subcategory == subcategory)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if bluebook_only:
        query = query.filter(Question.is_bluebook == True)

    count = query.count()
    return jsonify({"count": count}), 200


@questions_bp.route('/stats/by-subcategory', methods=['GET'])
def get_questions_stats_by_subcategory():
    """Get question count grouped by subcategory."""
    from sqlalchemy import func

    section = request.args.get('section')
    if not section:
        return jsonify({"detail": "Section parameter is required"}), 400

    db = get_db_session()

    results = db.query(
        Question.subcategory,
        func.count(Question.id).label('count')
    ).filter(
        Question.section == section,
        Question.subcategory.isnot(None)
    ).group_by(
        Question.subcategory
    ).all()

    return jsonify({
        "section": section,
        "stats": [
            {"subcategory": row.subcategory, "count": row.count}
            for row in results
        ]
    }), 200


@questions_bp.route('/seed', methods=['POST'])
def seed_questions():
    """Bulk insert questions from parsed JSON data.

    Expects JSON body: {"questions": [...], "secret": "seed-key"}
    Each question: {section, category, subcategory, difficulty,
                    question_text, choices, correct_answer,
                    explanation, passage_text, is_bluebook}
    """
    data = request.get_json()
    if not data:
        return jsonify({"detail": "No JSON body"}), 400

    seed_secret = data.get("secret", "")
    if seed_secret != "edunexus-seed-2024":
        return jsonify({"detail": "Invalid seed secret"}), 403

    questions_data = data.get("questions", [])
    if not questions_data:
        return jsonify({"detail": "No questions provided"}), 400

    db = get_db_session()

    inserted = 0
    skipped = 0
    errors = []

    try:
        for q in questions_data:
            try:
                # Map difficulty
                diff_val = q.get("difficulty", "medium").lower()
                try:
                    difficulty = DifficultyEnum(diff_val)
                except ValueError:
                    difficulty = DifficultyEnum.MEDIUM

                # Map correct answer
                ca_val = q.get("correct_answer", "").upper()
                try:
                    correct_answer = CorrectAnswerEnum(ca_val)
                except ValueError:
                    skipped += 1
                    continue

                # Map section
                sec_val = q.get("section", "english").lower()
                try:
                    section = SectionEnum(sec_val)
                except ValueError:
                    section = SectionEnum.ENGLISH

                # Serialize choices to JSON string for compatibility
                import json as _json
                choices_raw = q.get("choices", [])

                cat = q.get("category", "")
                subcat = q.get("subcategory", "")

                question = Question(
                    section=section,
                    topic=cat,          # Legacy field – mirror category
                    subtopic=subcat,    # Legacy field – mirror subcategory
                    category=cat,
                    subcategory=subcat,
                    difficulty=difficulty,
                    question_text=q.get("question_text", ""),
                    choices=choices_raw,
                    correct_answer=correct_answer,
                    explanation=q.get("explanation"),
                    passage_text=q.get("passage_text"),
                    is_bluebook=q.get("is_bluebook", True),
                    source_attribution=q.get(
                        "source_attribution",
                        "College Board SAT Question Bank"
                    ),
                )
                db.add(question)
                inserted += 1

                # Commit in batches
                if inserted % 100 == 0:
                    db.commit()

            except Exception as e:
                import traceback
                errors.append(f"Q#{inserted}: {str(e)} | {traceback.format_exc()[-200:]}")
                db.rollback()
                skipped += 1

        db.commit()

    except Exception as e:
        import traceback
        db.rollback()
        return jsonify({
            "detail": f"Seed failed: {str(e)}",
            "traceback": traceback.format_exc()[-500:],
            "inserted_before_error": inserted,
        }), 500

    return jsonify({
        "inserted": inserted,
        "skipped": skipped,
        "errors": errors[:10],  # First 10 errors only
    }), 201


@questions_bp.route('/seed/clear', methods=['DELETE'])
def clear_questions():
    """Clear all questions from the database. Use before re-seeding."""
    data = request.get_json() or {}
    if data.get("secret") != "edunexus-seed-2024":
        return jsonify({"detail": "Invalid seed secret"}), 403

    db = get_db_session()
    count = db.query(Question).count()
    db.query(Question).delete()
    db.commit()

    return jsonify({"deleted": count}), 200
