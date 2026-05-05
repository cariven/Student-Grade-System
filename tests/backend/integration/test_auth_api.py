import pytest


def test_register_success(client):
    """Happy path register → 201 + user dict."""
    res = client.post("/auth/register", json={
        "email": "new@test.com",
        "password": "password123"
    })
    assert res.status_code == 201
    assert "user" in res.get_json()


def test_register_duplicate_email(client):
    """Register email yang sama dua kali → 400 (ValueError dari service)."""
    payload = {"email": "dup@test.com", "password": "password123"}
    client.post("/auth/register", json=payload)
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_register_invalid_email(client):
    """Email bukan format valid → 400 (ValidationError dari validator)."""
    res = client.post("/auth/register", json={
        "email": "not-email",
        "password": "password123"
    })
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_register_short_password(client):
    """Password < 8 karakter → 400 (ValidationError dari validator)."""
    res = client.post("/auth/register", json={
        "email": "short@test.com",
        "password": "123"
    })
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_register_empty_email(client):
    """Email kosong → 400."""
    res = client.post("/auth/register", json={
        "email": "",
        "password": "password123"
    })
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_register_empty_password(client):
    """Password kosong → 400."""
    res = client.post("/auth/register", json={
        "email": "empty@test.com",
        "password": ""
    })
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_register_no_body(client):
    """Request tanpa body JSON → fallback ke {} → ValidationError email kosong."""
    res = client.post("/auth/register", json={})
    assert res.status_code == 400
    assert "error" in res.get_json()


# ──────────────────────────────────────────────
# LOGIN — ValidationError branch (sebelum _do_login)
# ──────────────────────────────────────────────

def test_login_invalid_email_format(client):
    """Email tidak valid saat login → 400 (ValidationError, tidak sampai _do_login)."""
    res = client.post("/auth/login", json={
        "email": "bukan-email",
        "password": "password123"
    })
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_login_empty_password(client):
    """Password kosong saat login → 400 (ValidationError)."""
    res = client.post("/auth/login", json={
        "email": "someone@test.com",
        "password": ""
    })
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_login_short_password(client):
    """Password < 8 karakter saat login → 400 (ValidationError)."""
    res = client.post("/auth/login", json={
        "email": "someone@test.com",
        "password": "123"
    })
    assert res.status_code == 400
    assert "error" in res.get_json()


# ──────────────────────────────────────────────
# LOGIN — _do_login: ValueError branch (line 34)
# ──────────────────────────────────────────────

def test_login_user_not_registered(client):
    """User belum register → login_user raise ValueError → 401."""
    res = client.post("/auth/login", json={
        "email": "notexist@test.com",
        "password": "password123"
    })
    assert res.status_code == 401
    assert "error" in res.get_json()


def test_login_wrong_password(client):
    """Password salah → bcrypt check gagal → ValueError → 401."""
    client.post("/auth/register", json={
        "email": "wrong@test.com",
        "password": "password123"
    })
    res = client.post("/auth/login", json={
        "email": "wrong@test.com",
        "password": "wrongpassword999"
    })
    assert res.status_code == 401
    assert "error" in res.get_json()


# ──────────────────────────────────────────────
# LOGIN — _do_login: happy path (line 35 — token return)
# ──────────────────────────────────────────────

def test_login_success(client):
    """Happy path login → 200 + token (cover line 35 _do_login)."""
    client.post("/auth/register", json={
        "email": "login@test.com",
        "password": "password123"
    })
    res = client.post("/auth/login", json={
        "email": "login@test.com",
        "password": "password123"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "token" in data
    assert data["message"] == "Login berhasil"


def test_login_success_token_is_string(client):
    """Pastikan token yang dikembalikan berupa string JWT."""
    client.post("/auth/register", json={
        "email": "tokencheck@test.com",
        "password": "password123"
    })
    res = client.post("/auth/login", json={
        "email": "tokencheck@test.com",
        "password": "password123"
    })
    token = res.get_json().get("token")
    assert isinstance(token, str)
    assert len(token) > 10  # JWT pasti panjang