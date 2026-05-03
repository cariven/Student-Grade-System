import bcrypt
from datetime import datetime, timezone
from .models import fetch_user_by_email, insert_user, fetch_user_by_id


def register_user(email: str, password: str) -> dict:
    """Daftarkan user baru. Raise ValueError jika email sudah ada."""
    existing = fetch_user_by_email(email)
    if existing:
        raise ValueError("Email sudah terdaftar.")

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    created_at = datetime.now(timezone.utc).isoformat()
    user_id = insert_user(email, password_hash, created_at)
    return {"id": user_id, "email": email}


def login_user(email: str, password: str) -> dict:
    """Login user. Raise ValueError jika email/password salah."""
    user = fetch_user_by_email(email)
    if not user:
        raise ValueError("Email atau password salah.")

    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        raise ValueError("Email atau password salah.")

    return user