from src.backend.app.auth_service import register_user, login_user

def test_register_success():
    assert register_user("user1", "123") == True

def test_register_duplicate():
    register_user("user2", "123")
    assert register_user("user2", "123") == False

def test_login_success():
    register_user("user3", "123")
    assert login_user("user3", "123") == True

def test_login_fail():
    assert login_user("wrong", "123") == False