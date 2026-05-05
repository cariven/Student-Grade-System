def test_home_endpoint(client):
    res = client.get("/")
    assert res.status_code == 200


def test_add_student_success(client, auth_headers):
    res = client.post("/students",
                      json={"name": "Budi"},
                      headers=auth_headers)
    assert res.status_code == 201
    assert res.get_json()["name"] == "Budi"


def test_add_student_empty_name(client, auth_headers):
    res = client.post("/students",
                      json={"name": ""},
                      headers=auth_headers)
    assert res.status_code == 400


def test_add_student_no_auth(client):
    res = client.post("/students", json={"name": "NoAuth"})
    assert res.status_code == 401


def test_get_students_empty(client, auth_headers):
    res = client.get("/students", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json() == []


def test_get_students_with_data(client, auth_headers):
    client.post("/students", json={"name": "Ani"}, headers=auth_headers)
    client.post("/students", json={"name": "Budi"}, headers=auth_headers)
    res = client.get("/students", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.get_json()) == 2


def test_get_students_no_auth(client):
    res = client.get("/students")
    assert res.status_code == 401


def test_delete_student_success(client, auth_headers):
    post_res = client.post("/students",
                           json={"name": "ToDelete"},
                           headers=auth_headers)
    student_id = post_res.get_json()["id"]
    res = client.delete(f"/students/{student_id}", headers=auth_headers)
    assert res.status_code == 200


def test_delete_student_not_found(client, auth_headers):
    res = client.delete("/students/9999", headers=auth_headers)
    assert res.status_code == 404


def test_delete_student_forbidden(client, auth_headers):
    # User 1 bikin student
    post_res = client.post("/students",
                           json={"name": "UserOneStudent"},
                           headers=auth_headers)
    student_id = post_res.get_json()["id"]

    # User 2 register & login
    client.post("/auth/register", json={
        "email": "user2@test.com",
        "password": "password123"
    })
    login_res = client.post("/auth/login", json={
        "email": "user2@test.com",
        "password": "password123"
    })
    user2_token = login_res.get_json()["token"]

    # User 2 coba hapus student user 1
    res = client.delete(f"/students/{student_id}",
                        headers={"Authorization": f"Bearer {user2_token}"})
    assert res.status_code == 403



# ================================================================
# Coverage 100%: Cover __init__.py line 33, 37, 41-43 (error handlers)
# ================================================================

def test_value_error_handler_via_duplicate_register(client):
    """Trigger @app.errorhandler(ValueError) di __init__.py line 33."""
    # Register pertama — sukses
    client.post("/auth/register", json={
        "email": "valerrhandler@test.com",
        "password": "password123"
    })
    # Register kedua dengan email sama → ValueError → error handler return 400
    res = client.post("/auth/register", json={
        "email": "valerrhandler@test.com",
        "password": "password123"
    })
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_permission_error_handler(client, monkeypatch):
    """Trigger @app.errorhandler(PermissionError) di __init__.py line 37."""
    from src.backend.app import routes

    def raise_permission_error(*args, **kwargs):
        raise PermissionError("Akses ditolak dari test")

    # Override fetch_all_students → raise PermissionError
    monkeypatch.setattr(routes, "fetch_all_students", raise_permission_error)

    # Register & login
    client.post("/auth/register", json={
        "email": "permerr@test.com",
        "password": "password123"
    })
    login_res = client.post("/auth/login", json={
        "email": "permerr@test.com",
        "password": "password123"
    })
    token = login_res.get_json()["token"]

    # GET /students → PermissionError → handler 403
    res = client.get("/students",
                     headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403


def test_http_exception_handler_404(client):
    """Trigger HTTPException branch di __init__.py line 41-42."""
    res = client.get("/url-yang-tidak-ada-xyz-12345")
    assert res.status_code == 404
    assert "error" in res.get_json()


def test_generic_exception_handler_500(client, monkeypatch):
    """Trigger generic Exception branch di __init__.py line 43 → 500."""
    from src.backend.app import routes

    def broken_db(*args, **kwargs):
        raise RuntimeError("Database broken unexpectedly!")

    monkeypatch.setattr(routes, "fetch_all_students", broken_db)

    # Register & login
    client.post("/auth/register", json={
        "email": "exc500test@test.com",
        "password": "password123"
    })
    login_res = client.post("/auth/login", json={
        "email": "exc500test@test.com",
        "password": "password123"
    })
    token = login_res.get_json()["token"]

    res = client.get("/students",
                     headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 500
    assert "error" in res.get_json()



# ================================================================
# Coverage 100%: Force trigger handle_value_error di __init__.py line 33
# ================================================================

def test_force_trigger_value_error_handler_via_grade(client, monkeypatch):
    """Force raise ValueError dari route untuk trigger error handler global."""
    from src.backend.app import routes

    def raise_value_error(*args, **kwargs):
        raise ValueError("Forced ValueError for coverage test")

    # Patch fetch_student_by_id → raise ValueError saat POST /grades
    monkeypatch.setattr(routes, "fetch_student_by_id", raise_value_error)

    # Register & login
    client.post("/auth/register", json={
        "email": "valerrforce@test.com",
        "password": "password123"
    })
    login_res = client.post("/auth/login", json={
        "email": "valerrforce@test.com",
        "password": "password123"
    })
    token = login_res.get_json()["token"]

    # Bikin student
    student_res = client.post("/students", json={"name": "Test"},
                              headers={"Authorization": f"Bearer {token}"})
    sid = student_res.get_json()["id"]

    # POST /grades → fetch_student_by_id raise ValueError → handler 400
    res = client.post("/grades", json={
        "student_id": sid, "tugas": 80, "uts": 80, "uas": 80
    }, headers={"Authorization": f"Bearer {token}"})
    
    assert res.status_code == 400
    assert "error" in res.get_json()