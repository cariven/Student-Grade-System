import re
from datetime import datetime


class ValidationError(ValueError):
    pass


def validate_title(title):
    if not title or not str(title).strip():
        raise ValidationError("Title tidak boleh kosong.")
    if len(str(title).strip()) > 200:
        raise ValidationError("Title maksimal 200 karakter.")
    return str(title).strip()


def validate_status(status):
    valid = {"pending", "in_progress", "done"}
    if status not in valid:
        raise ValidationError(f"Status harus salah satu dari: {', '.join(valid)}.")
    return status


def validate_email(email):
    if not email or not str(email).strip():
        raise ValidationError("Email tidak boleh kosong.")
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, str(email).strip()):
        raise ValidationError("Format email tidak valid.")
    return str(email).strip().lower()


def validate_password(password):
    if not password or not str(password).strip():
        raise ValidationError("Password tidak boleh kosong.")
    if len(str(password)) < 8:
        raise ValidationError("Password minimal 8 karakter.")
    return str(password)


def validate_deadline(deadline):
    if deadline is None or deadline == "":
        return None
    try:
        dt = datetime.fromisoformat(str(deadline))
        return dt.isoformat()
    except ValueError:
        raise ValidationError("Format deadline tidak valid. Gunakan format ISO 8601.")