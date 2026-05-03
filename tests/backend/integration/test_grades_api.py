def _create_student(client, auth_headers, name="TestStudent"):
    res = client.post("/students", json={"name": name}, headers=auth_headers)
    return res.get_json()["id"]


def test_add_grade_success(client, auth_headers):
    sid = _create_student(client, auth_headers)
    res = client.post("/grades", json={
        "student_id": sid, "tugas": 80, "uts": 70, "uas": 90
    }, headers=auth_headers)
    assert res.status_code == 201
    data = res.get_json()
    assert data["grade"] == "B"
    assert data["final"] == 81.0


def test_add_grade_missing_fields(client, auth_headers):
    sid = _create_student(client, auth_headers)
    res = client.post("/grades", json={
        "student_id": sid, "tugas": 80
    }, headers=auth_headers)
    assert res.status_code == 400


def test_add_grade_out_of_range(client, auth_headers):
    sid = _create_student(client, auth_headers)
    res = client.post("/grades", json={
        "student_id": sid, "tugas": 200, "uts": 70, "uas": 90
    }, headers=auth_headers)
    assert res.status_code == 400


def test_add_grade_negative(client, auth_headers):
    sid = _create_student(client, auth_headers)
    res = client.post("/grades", json={
        "student_id": sid, "tugas": -1, "uts": 70, "uas": 90
    }, headers=auth_headers)
    assert res.status_code == 400


def test_add_grade_student_not_found(client, auth_headers):
    res = client.post("/grades", json={
        "student_id": 9999, "tugas": 80, "uts": 70, "uas": 90
    }, headers=auth_headers)
    assert res.status_code == 404


def test_get_student_grades(client, auth_headers):
    sid = _create_student(client, auth_headers)
    client.post("/grades", json={
        "student_id": sid, "tugas": 85, "uts": 85, "uas": 85
    }, headers=auth_headers)
    res = client.get(f"/students/{sid}/grades", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_get_all_grades(client, auth_headers):
    sid = _create_student(client, auth_headers)
    client.post("/grades", json={
        "student_id": sid, "tugas": 90, "uts": 90, "uas": 90
    }, headers=auth_headers)
    res = client.get("/grades", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.get_json()) >= 1


def test_delete_grade(client, auth_headers):
    sid = _create_student(client, auth_headers)
    post_res = client.post("/grades", json={
        "student_id": sid, "tugas": 80, "uts": 80, "uas": 80
    }, headers=auth_headers)
    gid = post_res.get_json()["id"]
    res = client.delete(f"/grades/{gid}", headers=auth_headers)
    assert res.status_code == 200