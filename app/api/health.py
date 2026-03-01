from flask import Blueprint, jsonify
from sqlalchemy import text
from datetime import datetime
from app.api.utils import get_db_session

health_bp = Blueprint('health', __name__, url_prefix='/api/health')


@health_bp.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        db = get_db_session()
        result = db.execute(text("SELECT 1")).scalar()
        db_status = "healthy" if result == 1 else "unhealthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return jsonify({
        "status": "healthy" if db_status == "healthy" else "degraded",
        "api": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
    }), 200
