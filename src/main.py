import os

from flask import Flask

from src.api.emergency.routes import emergency_bp


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(emergency_bp, url_prefix="/api/emergency")

    @app.route("/")
    def index():
        return {"status": "ok", "service": "Emergency Resource API"}

    return app


if __name__ == "__main__":
    app = create_app()
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))
    app.run(host=host, port=port)
