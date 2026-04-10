from src.exercise.validators import is_valid_email
from src.exercise.validators import is_valid_password
from src.exercise.validators import is_valid_age


# Test Fonction1 : isValidEmail
def test_should_return_true_when_email_has_standard_address():
    assert is_valid_email("user@example.com") is True


def test_should_return_true_when_email_has_plus_sign_and_subdomain():
    assert is_valid_email("user.name+tag@domain.co") is True


def test_should_return_false_when_email_has_no_at_sign():
    assert is_valid_email("invalid") is False


def test_should_return_false_when_email_is_missing_user_part():
    assert is_valid_email("@domain.com") is False


def test_should_return_false_when_email_has_missing_domain_part():
    assert is_valid_email("user@") is False


def test_should_return_false_when_email_is_empty_string():
    assert is_valid_email("") is False


def test_should_return_false_when_email_is_none():
    assert is_valid_email(None) is False


# Fonction 2 : isValidPassword(password)
def test_should_return_true_when_password_meets_all_requirements():
    response = is_valid_password("Passw0rd!")
    assert response["valid"] is True
    assert len(response["errors"]) == 0


def test_should_return_false_when_password_is_too_short():
    response = is_valid_password("short")
    assert response["valid"] is False
    assert "trop court" in response["errors"]


def test_should_return_false_when_password_has_no_uppercase():
    response = is_valid_password("alllowercase1!")
    assert response["valid"] is False
    assert "pas de majuscule" in response["errors"]


def test_should_return_false_when_password_has_no_lowercase():
    response = is_valid_password("ALLUPPERCASE1!")
    assert response["valid"] is False
    assert "pas de miniscule" in response["errors"]


def test_should_return_false_when_password_has_no_digit():
    response = is_valid_password("NoDigits!here")
    assert response["valid"] is False
    assert "pas de chiffre" in response["errors"]


def test_should_return_false_when_password_has_no_special_character():
    response = is_valid_password("oSpecial1here")
    assert response["valid"] is False
    assert "pas de special" in response["errors"]


def test_should_return_false_when_password_is_none():
    response = is_valid_password(None)
    assert response["valid"] is False


def test_should_return_false_when_password_is_empty_string():
    response = is_valid_password(None)
    assert response["valid"] is False


# Fonction 3 : isValidAge(age)


def test_should_return_true_when_age_is_standard_adult_value():
    assert is_valid_age(25) is True


def test_should_return_true_when_age_is_at_minimum_boundary_zero():
    assert is_valid_age(0) is True


def test_should_return_true_when_age_is_at_maximum_boundary_150():
    assert is_valid_age(150) is True


def test_should_return_false_when_age_is_below_zero():
    assert is_valid_age(-1) is False


def test_should_return_false_when_age_is_above_150():
    assert is_valid_age(151) is False


def test_should_return_false_when_age_is_a_float():
    assert is_valid_age(25.5) is False


def test_should_return_false_when_age_is_a_string():
    assert is_valid_age("25") is False


def test_should_return_false_when_age_is_none():
    assert is_valid_age(None) is False
