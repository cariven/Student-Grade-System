import pytest
from src.backend.app.validators import (
    validate_email, validate_password, validate_title,
    validate_status, validate_deadline, ValidationError
)


# ===== validate_email =====

def test_validate_email_valid():
    assert validate_email("user@test.com") == "user@test.com"


def test_validate_email_uppercase_normalized():
    assert validate_email("USER@TEST.COM") == "user@test.com"


def test_validate_email_with_spaces():
    assert validate_email("  user@test.com  ") == "user@test.com"


def test_validate_email_empty_raises():
    with pytest.raises(ValidationError):
        validate_email("")


def test_validate_email_invalid_format_raises():
    with pytest.raises(ValidationError):
        validate_email("not-an-email")


def test_validate_email_missing_at_raises():
    with pytest.raises(ValidationError):
        validate_email("user.test.com")


# ===== validate_password =====

def test_validate_password_valid():
    assert validate_password("password123") == "password123"


def test_validate_password_too_short_raises():
    with pytest.raises(ValidationError):
        validate_password("short")


def test_validate_password_empty_raises():
    with pytest.raises(ValidationError):
        validate_password("")


def test_validate_password_exactly_8_chars():
    assert validate_password("12345678") == "12345678"


# ===== validate_title =====

def test_validate_title_valid():
    assert validate_title("My Title") == "My Title"


def test_validate_title_empty_raises():
    with pytest.raises(ValidationError):
        validate_title("")


def test_validate_title_too_long_raises():
    with pytest.raises(ValidationError):
        validate_title("x" * 201)


# ===== validate_status =====

def test_validate_status_valid():
    assert validate_status("pending") == "pending"


def test_validate_status_invalid_raises():
    with pytest.raises(ValidationError):
        validate_status("invalid")


# ===== validate_deadline =====

def test_validate_deadline_none():
    assert validate_deadline(None) is None


def test_validate_deadline_empty():
    assert validate_deadline("") is None


def test_validate_deadline_valid_iso():
    result = validate_deadline("2024-12-31T23:59:59")
    assert "2024-12-31" in result


def test_validate_deadline_invalid_raises():
    with pytest.raises(ValidationError):
        validate_deadline("not-a-date")