"""Digital SAT Score Calculator API."""
from flask import Blueprint, request, jsonify
from app.utils.score_calculator import DigitalSATScoreCalculator

scores_bp = Blueprint('scores', __name__, url_prefix='/api/scores')


@scores_bp.route('/calculate', methods=['POST'])
def calculate_score():
    """Calculate Digital SAT score estimation from module scores."""
    data = request.get_json()
    if not data:
        return jsonify({"detail": "Request body is required"}), 400

    # Validate required fields
    required = [
        'rw_module1_correct', 'rw_module2_correct', 'rw_module2_difficulty',
        'math_module1_correct', 'math_module2_correct', 'math_module2_difficulty'
    ]
    for field in required:
        if field not in data:
            return jsonify({"detail": f"Missing required field: {field}"}), 400

    # Validate numeric ranges
    try:
        rw_m1 = int(data['rw_module1_correct'])
        rw_m2 = int(data['rw_module2_correct'])
        math_m1 = int(data['math_module1_correct'])
        math_m2 = int(data['math_module2_correct'])
    except (ValueError, TypeError):
        return jsonify({"detail": "Module scores must be integers"}), 400

    rw_diff = data['rw_module2_difficulty']
    math_diff = data['math_module2_difficulty']

    if rw_diff not in ('easy', 'medium', 'hard') or math_diff not in ('easy', 'medium', 'hard'):
        return jsonify({"detail": "Difficulty must be 'easy', 'medium', or 'hard'"}), 400

    try:
        result = DigitalSATScoreCalculator.calculate_score(
            rw_module1_correct=rw_m1,
            rw_module2_correct=rw_m2,
            rw_module2_difficulty=rw_diff,
            math_module1_correct=math_m1,
            math_module2_correct=math_m2,
            math_module2_difficulty=math_diff,
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"detail": str(e)}), 400
    except Exception as e:
        return jsonify({"detail": f"Error calculating score: {str(e)}"}), 500
