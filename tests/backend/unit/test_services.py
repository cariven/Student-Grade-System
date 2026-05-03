from src.backend.app.services import (
    calculate_final,
    get_grade,
    create_student,
    create_grade,
    get_grades_by_student
)

def test_calculate_final_full():
    assert calculate_final(100, 100, 100) == 100

def test_calculate_final_zero():
    assert calculate_final(0, 0, 0) == 0

def test_calculate_final_random():
    assert calculate_final(80, 70, 90) == 81.0

def test_grade_A():
    assert get_grade(90) == "A"

def test_grade_B():
    assert get_grade(75) == "B"

def test_grade_C():
    assert get_grade(60) == "C"

def test_grade_D():
    assert get_grade(45) == "D"

def test_grade_E():
    assert get_grade(10) == "E"

def test_create_student():
    s = create_student("Budi")
    assert s["name"] == "Budi"

def test_create_grade():
    s = create_student("Ani")
    g = create_grade(s["id"], 80, 80, 80)
    assert g["final"] == 80

def test_get_grades_by_student():
    s = create_student("Test")
    create_grade(s["id"], 50, 50, 50)
    result = get_grades_by_student(s["id"])
    assert len(result) >= 1