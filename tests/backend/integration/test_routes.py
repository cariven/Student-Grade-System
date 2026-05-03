import pytest
from src.backend.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200

def test_add_student(client):
    res = client.post("/students", json={"name": "Budi"})
    assert res.status_code == 200

def test_get_students(client):
    res = client.get("/students")
    assert res.status_code == 200

def test_add_grade(client):
    client.post("/students", json={"name": "Ani"})
    res = client.post("/grades", json={
        "student_id": 1,
        "tugas": 80,
        "uts": 80,
        "uas": 80
    })
    assert res.status_code == 200

def test_invalid_grade(client):
    res = client.post("/grades", json={
        "student_id": 1,
        "tugas": 200,
        "uts": 80,
        "uas": 80
    })
    assert res.status_code == 400