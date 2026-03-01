from flask import Flask, jsonify
from flask_cors import CORS
from app.core.config import settings
from app.api.utils import close_db_session
from app.api import (
    auth_bp,
    questions_bp,
    practice_bp,
    tests_bp,
    health_bp,
    dashboard_bp,
    bookmarks_bp,
    import_questions_bp,
    mistakes_bp,
    scores_bp,
)


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Configure CORS - Allow all origins for development
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Register teardown to close DB sessions
    app.teardown_appcontext(close_db_session)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(practice_bp)
    app.register_blueprint(tests_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(bookmarks_bp)
    app.register_blueprint(import_questions_bp)
    app.register_blueprint(mistakes_bp)
    app.register_blueprint(scores_bp)

    @app.route("/")
    def root():
        """Root endpoint."""
        return jsonify({
            "message": "Welcome to EduNexus API",
            "version": "1.0.0",
        })

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.ENVIRONMENT == "development",
    )
