from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from .models import (
    insert_student, fetch_all_students, fetch_student_by_id, delete_student_by_id,
    insert_grade, fetch_grades_by_student, fetch_all_grades, delete_grade_by_id
)
from .services import calculate_final, get_grade

tasks_bp = Blueprint("main", __name__)


def now():
    return datetime.now(timezone.utc).isoformat()


@tasks_bp.route("/")
def home():
    return jsonify({"message": "Student Grade System API Running"}), 200


@tasks_bp.route("/students", methods=["POST"])
@jwt_required()
def add_student():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Nama tidak boleh kosong"}), 400
    student_id = insert_student(user_id, name, now())
    return jsonify({"id": student_id, "name": name}), 201


@tasks_bp.route("/students", methods=["GET"])
@jwt_required()
def get_students():
    user_id = int(get_jwt_identity())
    students = fetch_all_students(user_id)
    return jsonify(students), 200


@tasks_bp.route("/students/<int:student_id>", methods=["DELETE"])
@jwt_required()
def remove_student(student_id):
    user_id = int(get_jwt_identity())
    student = fetch_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Mahasiswa tidak ditemukan"}), 404
    if student["user_id"] != user_id:
        return jsonify({"error": "Akses ditolak"}), 403
    delete_student_by_id(student_id)
    return jsonify({"message": "Mahasiswa berhasil dihapus"}), 200


@tasks_bp.route("/grades", methods=["POST"])
@jwt_required()
def add_grade():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    student_id = data.get("student_id")
    tugas = data.get("tugas")
    uts = data.get("uts")
    uas = data.get("uas")

    if not all([student_id, tugas is not None, uts is not None, uas is not None]):
        return jsonify({"error": "student_id, tugas, uts, uas wajib diisi"}), 400

    for val in [tugas, uts, uas]:
        if not (0 <= float(val) <= 100):
            return jsonify({"error": "Nilai harus antara 0 dan 100"}), 400

    student = fetch_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Mahasiswa tidak ditemukan"}), 404

    final = calculate_final(float(tugas), float(uts), float(uas))
    grade = get_grade(final)
    grade_id = insert_grade(student_id, user_id, tugas, uts, uas, final, grade, now())

    return jsonify({
        "id": grade_id,
        "student_id": student_id,
        "tugas": tugas,
        "uts": uts,
        "uas": uas,
        "final": final,
        "grade": grade
    }), 201


@tasks_bp.route("/students/<int:student_id>/grades", methods=["GET"])
@jwt_required()
def get_student_grades(student_id):
    grades = fetch_grades_by_student(student_id)
    return jsonify(grades), 200


@tasks_bp.route("/grades", methods=["GET"])
@jwt_required()
def get_all_grades():
    user_id = int(get_jwt_identity())
    grades = fetch_all_grades(user_id)
    return jsonify(grades), 200


@tasks_bp.route("/grades/<int:grade_id>", methods=["DELETE"])
@jwt_required()
def remove_grade(grade_id):
    delete_grade_by_id(grade_id)
    return jsonify({"message": "Nilai berhasil dihapus"}), 200