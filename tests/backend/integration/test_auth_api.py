def test_register_success(client):
    res = client.post("/auth/register", json={
        "email": "new@test.com",
        "password": "password123"
    })
    assert res.status_code == 201
    assert "user" in res.get_json()


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "email": "dup@test.com",
        "password": "password123"
    })
    res = client.post("/auth/register", json={
        "email": "dup@test.com",
        "password": "password123"
    })
    assert res.status_code == 400


def test_register_invalid_email(client):
    res = client.post("/auth/register", json={
        "email": "not-email",
        "password": "password123"
    })
    assert res.status_code == 400


def test_register_short_password(client):
    res = client.post("/auth/register", json={
        "email": "short@test.com",
        "password": "123"
    })
    assert res.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={
        "email": "login@test.com",
        "password": "password123"
    })
    res = client.post("/auth/login", json={
        "email": "login@test.com",
        "password": "password123"
    })
    assert res.status_code == 200
    assert "token" in res.get_json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "wrong@test.com",
        "password": "password123"
    })
    res = client.post("/auth/login", json={
        "email": "wrong@test.com",
        "password": "wrongpass123"
    })
    assert res.status_code == 401


def test_login_not_registered(client):
    res = client.post("/auth/login", json={
        "email": "notexist@test.com",
        "password": "password123"
    })
    assert res.status_code == 401