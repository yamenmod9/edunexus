from flask import Blueprint, request, jsonify
from app.api.utils import get_db_session, get_current_user, login_required, user_to_dict
from app.models import User
from app.core import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    if not data:
        return jsonify({"detail": "Request body is required"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"detail": "Email and password are required"}), 400

    if len(password) < 8:
        return jsonify({"detail": "Password must be at least 8 characters"}), 400

    db = get_db_session()

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return jsonify({"detail": "Email already registered"}), 400

    # Create new user
    hashed_password = get_password_hash(password)
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=data.get("full_name"),
    )

    # Set optional fields
    if data.get("sat_exam_date"):
        from datetime import date
        try:
            new_user.sat_exam_date = date.fromisoformat(data["sat_exam_date"])
        except (ValueError, TypeError):
            pass

    if data.get("target_score"):
        new_user.target_score = data["target_score"]

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return jsonify(user_to_dict(new_user)), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens."""
    data = request.get_json()
    if not data:
        return jsonify({"detail": "Request body is required"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"detail": "Email and password are required"}), 400

    db = get_db_session()

    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return jsonify({"detail": "Incorrect email or password"}), 401

    if not user.is_active:
        return jsonify({"detail": "User account is inactive"}), 403

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token."""
    data = request.get_json()
    if not data or not data.get("refresh_token"):
        return jsonify({"detail": "Refresh token is required"}), 400

    payload = decode_token(data["refresh_token"])

    if not payload or payload.get("type") != "refresh":
        return jsonify({"detail": "Invalid refresh token"}), 401

    user_id = payload.get("sub")
    if not user_id:
        return jsonify({"detail": "Invalid refresh token"}), 401

    db = get_db_session()

    # Verify user exists
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        return jsonify({"detail": "User not found or inactive"}), 401

    # Create new tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return jsonify({
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }), 200


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_me():
    """Get current user information."""
    from flask import g
    return jsonify(user_to_dict(g.current_user)), 200
