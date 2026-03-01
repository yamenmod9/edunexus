"""Shared authentication utilities for Flask blueprints."""
from functools import wraps
from flask import request, jsonify, g
from app.db import SessionLocal
from app.models import User
from app.core.security import decode_token


def get_db_session():
    """Get a database session, storing it on Flask's g object for the request."""
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db


def close_db_session(exception=None):
    """Close the database session at the end of a request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def get_current_user(token: str, db) -> User:
    """Get current user from JWT token."""
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return None

    user = db.query(User).filter(User.id == user_id_int).first()
    return user


def login_required(f):
    """Decorator that requires a valid JWT token and injects current_user."""
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")
        if not authorization.startswith("Bearer "):
            return jsonify({"detail": "Missing or invalid authorization header"}), 401

        token = authorization.replace("Bearer ", "")
        db = get_db_session()
        user = get_current_user(token, db)

        if not user:
            return jsonify({"detail": "Invalid or expired token"}), 401

        g.current_user = user
        return f(*args, **kwargs)
    return decorated


def user_to_dict(user: User) -> dict:
    """Serialize a User model to a dict for JSON responses."""
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "sat_exam_date": user.sat_exam_date.isoformat() if user.sat_exam_date else None,
        "target_score": user.target_score,
    }
