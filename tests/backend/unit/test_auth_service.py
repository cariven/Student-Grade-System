import pytest
from src.backend.app.auth_service import register_user, login_user


def test_register_user_success(app):
    with app.app_context():
        user = register_user("new@test.com", "password123")
        assert user["email"] == "new@test.com"
        assert "id" in user


def test_register_user_duplicate_raises(app):
    with app.app_context():
        register_user("dup@test.com", "password123")
        with pytest.raises(ValueError, match="sudah terdaftar"):
            register_user("dup@test.com", "password123")


def test_login_user_success(app):
    with app.app_context():
        register_user("login@test.com", "password123")
        user = login_user("login@test.com", "password123")
        assert user["email"] == "login@test.com"


def test_login_user_wrong_password_raises(app):
    with app.app_context():
        register_user("wrong@test.com", "password123")
        with pytest.raises(ValueError, match="salah"):
            login_user("wrong@test.com", "wrongpassword")


def test_login_user_not_found_raises(app):
    with app.app_context():
        with pytest.raises(ValueError, match="salah"):
            login_user("notexist@test.com", "password123")


def test_register_password_is_hashed(app):
    with app.app_context():
        from src.backend.app.models import fetch_user_by_email
        register_user("hash@test.com", "password123")
        user = fetch_user_by_email("hash@test.com")
        assert user["password_hash"] != "password123"


def test_login_returns_user_dict(app):
    with app.app_context():
        register_user("dict@test.com", "password123")
        user = login_user("dict@test.com", "password123")
        assert isinstance(user, dict)
        assert "id" in user
        assert "password_hash" in user



def test_fetch_user_by_id_exists(app):
    """Cover fetch_user_by_id dengan user valid (line 72-75)."""
    from src.backend.app.models import insert_user, fetch_user_by_id
    with app.app_context():
        uid = insert_user("fetchbyid@test.com", "hashed_pwd", "2026-01-01T00:00:00")
        user = fetch_user_by_id(uid)
        assert user is not None
        assert user["email"] == "fetchbyid@test.com"
        assert user["id"] == uid


def test_fetch_user_by_id_not_found(app):
    """Cover fetch_user_by_id dengan id tidak ada → None."""
    from src.backend.app.models import fetch_user_by_id
    with app.app_context():
        user = fetch_user_by_id(99999)
        assert user is None