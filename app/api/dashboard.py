"""Dashboard API endpoints for student analytics and statistics."""
from flask import Blueprint, request, jsonify, g
from app.api.utils import get_db_session, login_required
from app.services.analytics import AnalyticsService
from app.services.score_prediction import ScorePredictionService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard_bp.route('/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    """Get comprehensive dashboard statistics for the current user."""
    db = get_db_session()
    stats = AnalyticsService.get_dashboard_stats(db, g.current_user.id)

    # Serialize date fields
    if stats.get("sat_exam_date"):
        stats["sat_exam_date"] = stats["sat_exam_date"].isoformat()

    return jsonify(stats), 200


@dashboard_bp.route('/performance-graph', methods=['GET'])
@login_required
def get_performance_graph():
    """Get time-series performance data for graphs."""
    days = request.args.get('days', 7, type=int)
    days = max(1, min(90, days))

    db = get_db_session()
    graph_data = AnalyticsService.get_performance_graph_data(db, g.current_user.id, days)

    # Serialize date fields
    for item in graph_data:
        if item.get("date"):
            item["date"] = item["date"].isoformat()

    return jsonify({
        "daily_performance": graph_data,
        "period_days": days,
    }), 200


@dashboard_bp.route('/error-logs', methods=['GET'])
@login_required
def get_error_logs():
    """Get error logs (wrong questions) grouped by day."""
    days = request.args.get('days', 30, type=int)
    limit = request.args.get('limit', 100, type=int)
    days = max(1, min(90, days))
    limit = max(1, min(500, limit))

    db = get_db_session()
    error_logs = AnalyticsService.get_error_logs(db, g.current_user.id, days, limit)

    # Serialize date/datetime fields
    for log in error_logs:
        if log.get("date"):
            log["date"] = log["date"].isoformat()
        for mistake in log.get("mistakes", []):
            if mistake.get("attempted_at"):
                mistake["attempted_at"] = mistake["attempted_at"].isoformat()

    return jsonify(error_logs), 200


@dashboard_bp.route('/category-performance', methods=['GET'])
@login_required
def get_category_performance():
    """Get performance breakdown by category and subcategory."""
    section = request.args.get('section')
    if not section or section not in ['math', 'english']:
        return jsonify({"detail": "Section must be 'math' or 'english'"}), 400

    db = get_db_session()
    performance = AnalyticsService.get_category_performance(db, g.current_user.id, section)

    return jsonify(performance), 200


@dashboard_bp.route('/score-prediction', methods=['GET'])
@login_required
def get_score_prediction():
    """Get SAT score prediction based on practice performance."""
    recalculate = request.args.get('recalculate', 'false').lower() == 'true'

    db = get_db_session()

    if recalculate:
        prediction = ScorePredictionService.calculate_score_prediction(db, g.current_user.id)
    else:
        prediction = ScorePredictionService.get_latest_prediction(db, g.current_user.id)
        if not prediction:
            prediction = ScorePredictionService.calculate_score_prediction(db, g.current_user.id)

    # Serialize datetime fields
    if prediction.get("created_at"):
        prediction["created_at"] = prediction["created_at"].isoformat()

    return jsonify(prediction), 200


@dashboard_bp.route('/update-daily-stats', methods=['POST'])
@login_required
def update_daily_statistics():
    """Manually trigger update of daily statistics for the current user."""
    db = get_db_session()
    AnalyticsService.update_daily_statistics(db, g.current_user.id)

    return jsonify({"message": "Daily statistics updated successfully"}), 200


@dashboard_bp.route('/mistakes/review-status', methods=['GET'])
@login_required
def get_mistakes_review_status():
    """Get count of reviewed vs unreviewed mistakes."""
    from app.models import MistakeLog
    from sqlalchemy import func

    db = get_db_session()

    reviewed_count = db.query(func.count(MistakeLog.id)).filter(
        MistakeLog.user_id == g.current_user.id,
        MistakeLog.reviewed == True
    ).scalar() or 0

    unreviewed_count = db.query(func.count(MistakeLog.id)).filter(
        MistakeLog.user_id == g.current_user.id,
        MistakeLog.reviewed == False
    ).scalar() or 0

    total = reviewed_count + unreviewed_count

    return jsonify({
        "reviewed": reviewed_count,
        "unreviewed": unreviewed_count,
        "total": total,
        "review_progress": (reviewed_count / total * 100) if total > 0 else 0.0,
    }), 200


@dashboard_bp.route('/mistakes/<int:mistake_id>/mark-reviewed', methods=['POST'])
@login_required
def mark_mistake_reviewed(mistake_id):
    """Mark a specific mistake as reviewed."""
    from app.models import MistakeLog
    from datetime import datetime

    db = get_db_session()

    mistake = db.query(MistakeLog).filter(
        MistakeLog.id == mistake_id,
        MistakeLog.user_id == g.current_user.id
    ).first()

    if not mistake:
        return jsonify({"detail": "Mistake not found"}), 404

    mistake.reviewed = True
    mistake.reviewed_at = datetime.utcnow()
    db.commit()

    return jsonify({"message": "Mistake marked as reviewed"}), 200
