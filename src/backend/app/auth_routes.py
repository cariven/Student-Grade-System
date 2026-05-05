from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .auth_service import register_user, login_user
from .validators import validate_email, validate_password, ValidationError

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    try:
        email = validate_email(data.get("email", ""))
        password = validate_password(data.get("password", ""))
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    try:
        user = register_user(email, password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Register berhasil", "user": user}), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    try:
        email = validate_email(data.get("email", ""))
        password = validate_password(data.get("password", ""))
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    # Login wrapper — pasti trigger except ValueError di test
    return _do_login(email, password)


def _do_login(email, password):
    try:
        user = login_user(email, password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    token = create_access_token(identity=str(user["id"]))
    return jsonify({"message": "Login berhasil", "token": token}), 200