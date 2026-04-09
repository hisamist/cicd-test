# Met la premiere lettre en majuscule, le reste en minuscule.
def capitalize(word: str) -> str:
    if word is None:
        return ""
    if not isinstance(word, str):
        word = str(word)
    return word.strip().capitalize()


# Calcule la moyenne d'un tableau de nombres, arrondie a 2 decimales.
def calculateAverage(numbers: list[int]) -> int:
    if not numbers:
        return 0

    total_number = len(numbers)
    sum_number = sum(numbers)
    average = sum_number / total_number

    return int(round(average))


# Transforme un texte en slug URL : minuscules, espaces remplaces par des tirets,
# caratcteres, speciaux supprimes
def slugify(text: str) -> str:
    if text is None:
        return ""
    response = text.strip().lower().replace(" ", "-").replace("'", "").replace("!", "")
    if response.endswith("-"):
        response = response[:-1]
    return response


# Limite une valeur entre un minimum et un maximum.
def clamp(value: int, min: int, max: int) -> int:
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value


# sort_students:
def sort_students(students, sort_by, order="asc"):
    if not students:
        return []
    is_reverse = order == "desc"
    return sorted(students, key=lambda x: x[sort_by], reverse=is_reverse)


# Convertit un prix sous differents formats en nombre. Ecrivez la fonction et ses tests.
def parse_price(input) -> float | None:
    if not input:
        return None
    try:
        input_str = str(input).strip()
        if input_str.lower() == "gratuit":
            return 0.0
        input_str = input_str.replace("€", "").replace("(nombre)", "").strip()
        input_str = input_str.replace(",", ".")
        response = float(input_str)
        if response < 0:
            return None
        return response
    except (ValueError, AttributeError):
        return None


# Regroupe un tableau d'objets par la valeur d'une cle. Ecrivez la fonction en TDD.
def group_by(members: list[dict], key: str):
    result = {}
    if not members or not key:
        raise ValueError("input required")

    for item in members:
        if key not in item:
            raise ValueError("unmatch key")
        k = item[key]
        result.setdefault(k, []).append(item["name"])
    return result
