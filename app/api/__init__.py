from app.api.auth import auth_bp
from app.api.questions import questions_bp
from app.api.practice import practice_bp
from app.api.tests import tests_bp
from app.api.health import health_bp
from app.api.dashboard import dashboard_bp
from app.api.bookmarks import bookmarks_bp
from app.api.import_questions import import_questions_bp
from app.api.mistakes import mistakes_bp
from app.api.scores import scores_bp

__all__ = [
    "auth_bp",
    "questions_bp",
    "practice_bp",
    "tests_bp",
    "health_bp",
    "dashboard_bp",
    "bookmarks_bp",
    "import_questions_bp",
    "mistakes_bp",
    "scores_bp",
]
