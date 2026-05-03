import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.backend.app import create_app
from src.backend.app.models import init_db


@pytest.fixture
def app():
    """Flask app dengan DB isolated per-test."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.environ["DATABASE"] = db_path

    app = create_app({"TESTING": True})

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)
    os.environ.pop("DATABASE", None)


@pytest.fixture
def client(app):
    """Test client Flask."""
    return app.test_client()


@pytest.fixture
def auth_token(client):
    """Register + login, return JWT token."""
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "password123"
    })
    res = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "password123"
    })
    return res.get_json()["token"]


@pytest.fixture
def auth_headers(auth_token):
    """Header dengan Authorization Bearer token."""
    return {"Authorization": f"Bearer {auth_token}"}