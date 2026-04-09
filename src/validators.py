# Retourne True si l'email est valide (contient @ et un domaine avec un point).


def is_valid_email(email: str) -> bool:
    if not email:
        return False
    if "@" not in email:
        return False

    parts = email.split("@")
    if len(parts) != 2:
        return False

    user, domain = parts

    if not user or not domain or "." not in domain:
        return False

    if domain.startswith(".") or domain.endswith("."):
        return False

    return True


"""
    # Retourne un objet { valid: boolean, errors: string[] }. Regles :
        • Minimum 8 caracteres
        • Au moins 1 majuscule
        • Au moins 1 minuscule
        • Au moins 1 chiffre
        • Au moins 1 caractere special (!@#$%^&*)
"""


def is_valid_password(pw: str):
    response = {"valid": False, "errors": []}
    if not pw:
        response["valid"] = False
        return response

    if len(pw) < 8:
        response["errors"].append("trop court")

    if not any(c.isupper() for c in pw):
        response["errors"].append("pas de majuscule")

    if not any(c.islower() for c in pw):
        response["errors"].append("pas de miniscule")

    if not any(c.isdigit() for c in pw):
        response["errors"].append("pas de chiffre")

    special_chars = "!@#$%^&*"
    if not any(char in special_chars for char in pw):
        response["errors"].append("pas de special")

    if len(response["errors"]) == 0:
        response["valid"] = True
    return response


# Retourne true si l'age est un entier entre 0 et 150
def is_valid_age(age: int) -> bool:
    if not age and age != 0:
        return False

    if not isinstance(age, int):
        return False

    if age > 150 or age < 0:
        return False

    return True
