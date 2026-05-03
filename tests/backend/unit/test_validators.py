from src.backend.app.validators import validate_score, validate_name

def test_valid_score():
    assert validate_score(50) == True

def test_invalid_score_negative():
    assert validate_score(-1) == False

def test_invalid_score_over():
    assert validate_score(101) == False

def test_invalid_score_type():
    assert validate_score("abc") == False

def test_valid_name():
    assert validate_name("Budi") == True

def test_invalid_name_empty():
    assert validate_name("") == False