from src.validators import is_valid_email
from src.validators import is_valid_password
from src.validators import is_valid_age

# Test Fonction1 : isValidEmail
def test_email_valid_standard():
   assert is_valid_email("user@example.com") is True

def test_email_valid_complex():
   assert is_valid_email("user.name+tag@domain.co") is True

def test_email_invalid():
   assert is_valid_email("invalid") is False

def test_email_without_user():
    assert is_valid_email("@domain.com") is False

def test_email_without_domain():
    assert is_valid_email("user@") is False

def test_email_empty_false():
   assert is_valid_email("") is False

def test_email_none_false():
   assert is_valid_email(None) is False


# Fonction 2 : isValidPassword(password)
def test_valid_password():
    response = is_valid_password("Passw0rd!")
    assert response["valid"] is True
    assert len(response["errors"]) ==0 

def test_valid_password_too_short():
    response = is_valid_password("short")
    assert response["valid"] is False
    assert "trop court" in response["errors"] 

def test_valid_password_without_maj():
    response = is_valid_password("alllowercase1!")
    assert response["valid"] is False
    assert "pas de majuscule" in response["errors"] 

def test_valid_password_without_miniscule():
    response = is_valid_password("ALLUPPERCASE1!")
    assert response["valid"] is False
    assert "pas de miniscule" in response["errors"] 

def test_valid_password_without_number():
    response = is_valid_password("NoDigits!here")
    assert response["valid"] is False
    assert "pas de chiffre" in response["errors"] 

def test_valid_password_without_special():
    response = is_valid_password("oSpecial1here")
    assert response["valid"] is False
    assert "pas de special" in response["errors"] 

def test_valid_password_none():
    response = is_valid_password(None)
    assert response["valid"] is False

def test_valid_password_empty():
    response = is_valid_password(None)
    assert response["valid"] is False

# Fonction 3 : isValidAge(age)

def test_valid_age_20():
    assert is_valid_age(25) is True

def test_valid_age_border_0():
    assert is_valid_age(0) is True

def test_valid_age_border_150():
    assert is_valid_age(150) is True

def test_valid_age_fewer_than_0():
    assert is_valid_age(-1) is False

def test_valid_age_over_150():
    assert is_valid_age(151) is False

def test_valid_age_not_int():
    assert is_valid_age(25.5) is False

def test_valid_age_not_number():
    assert is_valid_age("25") is False

def test_valid_age_null():
    assert is_valid_age(None) is False