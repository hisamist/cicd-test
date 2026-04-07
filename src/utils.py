# Met la premiere lettre en majuscule, le reste en minuscule.
def capitalize(word: str) -> str:
    if word is None:
        return ""
    if not isinstance(word, str):
        word = str(word)
    return word.strip().capitalize()

# Calcule la moyenne d'un tableau de nombres, arrondie a 2 decimales.
def calculateAverage(numbers:list[int])->int:
    if not numbers:
        return 0

    total_number = len(numbers)
    sum_number = sum(numbers)
    average = sum_number/total_number

    return int(round(average))


# Transforme un texte en slug URL : minuscules, espaces remplaces par des tirets, 
# caratcteres, speciaux supprimes
def slugify(text:str) -> str:
    if text is None:
        return ""
    response = text.strip().lower().replace(" ","-").replace("'","").replace("!","")
    if response.endswith("-"):
        response = response[:-1]
    return response

# Limite une valeur entre un minimum et un maximum.
def clamp(value:int,min:int, max:int) -> int:
    if value < min:
      return min
    elif value > max:
      return max
    else:
      return  value

# sort_students:
def sort_students(students,sort_by,order="asc"):
    if not students:
        return []
    is_reverse = (order == "desc")
    return sorted(students, key=lambda x: x[sort_by],reverse=is_reverse)


    