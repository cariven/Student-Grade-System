from src.backend.app.services import calculate_final, get_grade


# ===== calculate_final =====

def test_calculate_final_perfect():
    assert calculate_final(100, 100, 100) == 100.0


def test_calculate_final_zero():
    assert calculate_final(0, 0, 0) == 0.0


def test_calculate_final_normal():
    # 0.3*80 + 0.3*70 + 0.4*90 = 24 + 21 + 36 = 81
    assert calculate_final(80, 70, 90) == 81.0


def test_calculate_final_decimal():
    # 0.3*75.5 + 0.3*80.5 + 0.4*90.5 = 22.65 + 24.15 + 36.2 = 83.0
    assert calculate_final(75.5, 80.5, 90.5) == 83.0


def test_calculate_final_rounded():
    result = calculate_final(77, 83, 91)
    assert isinstance(result, float)
    assert result == round(result, 2)


# ===== get_grade =====

def test_get_grade_A_boundary():
    assert get_grade(85) == "A"


def test_get_grade_A_high():
    assert get_grade(100) == "A"


def test_get_grade_B_boundary():
    assert get_grade(70) == "B"


def test_get_grade_B_mid():
    assert get_grade(80) == "B"


def test_get_grade_C_boundary():
    assert get_grade(55) == "C"


def test_get_grade_C_mid():
    assert get_grade(65) == "C"


def test_get_grade_D_boundary():
    assert get_grade(40) == "D"


def test_get_grade_D_mid():
    assert get_grade(50) == "D"


def test_get_grade_E_low():
    assert get_grade(0) == "E"


def test_get_grade_E_just_below():
    assert get_grade(39) == "E"