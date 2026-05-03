import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException


def create_app(config=None):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY",
        "ganti-secret-key-ini-dengan-string-yang-panjang-dan-aman-min-32-karakter-untuk-production"
    )

    if config:
        app.config.update(config)

    CORS(app)
    JWTManager(app)

    from .models import init_db
    from .routes import tasks_bp
    from .auth_routes import auth_bp

    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        init_db()

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(PermissionError)
    def handle_permission(e):
        return jsonify({"error": str(e)}), 403

    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code
        return jsonify({"error": "Terjadi kesalahan internal pada server"}), 500

    return app


# Untuk backward compatibility dengan run.py
app = create_app()