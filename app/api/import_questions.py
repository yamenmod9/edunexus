"""Question import API endpoints for bulk question upload."""
from flask import Blueprint, request, jsonify, make_response
from app.api.utils import get_db_session
from app.services.question_importer import QuestionImporter, QuestionImportError

import_questions_bp = Blueprint('import_questions', __name__, url_prefix='/api/admin/questions')


@import_questions_bp.route('/import/csv', methods=['POST'])
def import_questions_csv():
    """Import questions from CSV file."""
    if 'file' not in request.files:
        return jsonify({"detail": "No file provided"}), 400

    file = request.files['file']
    if not file.filename or not file.filename.endswith('.csv'):
        return jsonify({"detail": "File must be a CSV file"}), 400

    try:
        content = file.read().decode('utf-8')
        db = get_db_session()
        success_count, errors = QuestionImporter.import_from_csv(content, db)

        return jsonify({
            "success": True,
            "message": f"Successfully imported {success_count} questions",
            "success_count": success_count,
            "error_count": len(errors),
            "errors": errors[:10] if errors else [],
        }), 200

    except QuestionImportError as e:
        return jsonify({"detail": str(e)}), 400
    except Exception as e:
        return jsonify({"detail": f"Import failed: {str(e)}"}), 500


@import_questions_bp.route('/import/json', methods=['POST'])
def import_questions_json():
    """Import questions from JSON file."""
    if 'file' not in request.files:
        return jsonify({"detail": "No file provided"}), 400

    file = request.files['file']
    if not file.filename or not file.filename.endswith('.json'):
        return jsonify({"detail": "File must be a JSON file"}), 400

    try:
        content = file.read().decode('utf-8')
        db = get_db_session()
        success_count, errors = QuestionImporter.import_from_json(content, db)

        return jsonify({
            "success": True,
            "message": f"Successfully imported {success_count} questions",
            "success_count": success_count,
            "error_count": len(errors),
            "errors": errors[:10] if errors else [],
        }), 200

    except QuestionImportError as e:
        return jsonify({"detail": str(e)}), 400
    except Exception as e:
        return jsonify({"detail": f"Import failed: {str(e)}"}), 500


@import_questions_bp.route('/import/template/csv', methods=['GET'])
def get_csv_template():
    """Download CSV template for question import."""
    template = QuestionImporter.get_csv_template()
    response = make_response(template)
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = "attachment; filename=question_import_template.csv"
    return response


@import_questions_bp.route('/import/template/json', methods=['GET'])
def get_json_template():
    """Download JSON template for question import."""
    template = QuestionImporter.get_json_template()
    response = make_response(template)
    response.headers["Content-Type"] = "application/json"
    response.headers["Content-Disposition"] = "attachment; filename=question_import_template.json"
    return response


@import_questions_bp.route('/validation-rules', methods=['GET'])
def get_validation_rules():
    """Get validation rules for question import."""
    return jsonify({
        "required_fields": QuestionImporter.REQUIRED_FIELDS,
        "optional_fields": QuestionImporter.OPTIONAL_FIELDS,
        "valid_sections": QuestionImporter.VALID_SECTIONS,
        "valid_difficulties": QuestionImporter.VALID_DIFFICULTIES,
        "valid_answers": QuestionImporter.VALID_ANSWERS,
        "english_categories": QuestionImporter.ENGLISH_CATEGORIES,
        "format_notes": {
            "section": "Must be 'math' or 'english'",
            "difficulty": "Must be 'easy', 'medium', or 'hard'",
            "correct_answer": "Must be 'A', 'B', 'C', or 'D'",
            "choices": "Must provide 4 choices (choice_a through choice_d in CSV, or array in JSON)",
            "is_bluebook": "Boolean value (true/false, yes/no, 1/0)",
            "category": "Required for English questions, should match SAT taxonomy",
            "subcategory": "Optional but recommended for English questions",
        },
    }), 200
