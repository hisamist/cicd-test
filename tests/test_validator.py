from src.validators import is_valid_email
from src.validators import is_valid_password
from src.validators import is_valid_age

# Test Fonction1 : isValidEmail
def test_is_valid_email_with_standard_address_returns_true():
   assert is_valid_email("user@example.com") is True

def test_is_valid_email_with_plus_sign_and_subdomain_returns_true():
   assert is_valid_email("user.name+tag@domain.co") is True

def test_is_valid_email_without_at_sign_returns_false():
   assert is_valid_email("invalid") is False

def test_is_valid_email_missing_user_part_returns_false():
    assert is_valid_email("@domain.com") is False

def test_is_valid_email_with_empty_string_returns_false():
    assert is_valid_email("user@") is False

def test_is_valid_email_with_empty_string_returns_false():
   assert is_valid_email("") is False

def test_is_valid_email_with_none_input_returns_false():
   assert is_valid_email(None) is False


# Fonction 2 : isValidPassword(password)
def test_is_valid_password_with_all_requirements_returns_true():
    response = is_valid_password("Passw0rd!")
    assert response["valid"] is True
    assert len(response["errors"]) ==0 

def test_is_valid_password_fails_if_too_short():
    response = is_valid_password("short")
    assert response["valid"] is False
    assert "trop court" in response["errors"] 

def test_is_valid_password_fails_without_uppercase():
    response = is_valid_password("alllowercase1!")
    assert response["valid"] is False
    assert "pas de majuscule" in response["errors"] 

def test_is_valid_password_fails_without_lowercase():
    response = is_valid_password("ALLUPPERCASE1!")
    assert response["valid"] is False
    assert "pas de miniscule" in response["errors"] 

def test_is_valid_password_fails_without_digit():
    response = is_valid_password("NoDigits!here")
    assert response["valid"] is False
    assert "pas de chiffre" in response["errors"] 

def test_is_valid_password_fails_without_special_character():
    response = is_valid_password("oSpecial1here")
    assert response["valid"] is False
    assert "pas de special" in response["errors"] 

def test_is_valid_password_with_none_input_returns_false():
    response = is_valid_password(None)
    assert response["valid"] is False

def test_is_valid_password_with_empty_string_returns_false():
    response = is_valid_password(None)
    assert response["valid"] is False

# Fonction 3 : isValidAge(age)

def test_is_valid_age_with_standard_adult_age_returns_true():
    assert is_valid_age(25) is True

def test_is_valid_age_at_minimum_boundary_zero_returns_true():
    assert is_valid_age(0) is True

def test_is_valid_age_at_maximum_boundary_150_returns_true():
    assert is_valid_age(150) is True

def test_is_valid_age_below_zero_returns_false():
    assert is_valid_age(-1) is False

def test_is_valid_age_above_150_returns_false():
    assert is_valid_age(151) is False

def test_is_valid_age_with_float_returns_false():
    assert is_valid_age(25.5) is False

def test_is_valid_age_with_string_input_returns_false():
    assert is_valid_age("25") is False

def test_is_valid_age_with_none_input_returns_false():
    assert is_valid_age(None) is False