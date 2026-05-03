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