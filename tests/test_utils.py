from src.utils import capitalize
from src.utils import calculateAverage
from src.utils import slugify
from src.utils import clamp

# Test Fonction 1 : capitalize
def test_capilize_lowercase():
    assert capitalize("hello") == "Hello"

def test_capitalize_uppercase():
    assert capitalize("WORLD") == "World"

def test_capitalize_empty_string():
    assert capitalize("") == ""

def test_capitalize_none():
    assert capitalize(None)== ""

# Test Fonction 2:calculateAverage(numbers)
def test_calculate_average_basic():
    assert calculateAverage([10,12,14]) == 12

def test_calculate_average_single_element():
    assert calculateAverage([15]) == 15

def test_calculate_average_empty_list():
    assert calculateAverage([]) == 0

def test_calculate_average_rounding():
    assert calculateAverage([10,11,12]) == 11

def test_calculate_average_none_imput():
    assert calculateAverage(None)== 0

# Test Fonction 3: slugify(text)
def test_slugify_basic():
    assert slugify("Hello World") =="hello-world"

def test_slugify_with_space():
    assert slugify(" Spaces Everywhere ") =="spaces-everywhere"

def test_slugify_with_special_chars():
    assert slugify("C'est l'ete !") =="cest-lete"

def test_slugify_empty():
    assert slugify(None) == ""

# Test Fonction 4: clamp(value, min, max)
def test_clamp_1():
    assert clamp(5, 0, 10) == 5

def test_clamp_2():
    assert clamp(-5, 0, 10) == 0

def test_clamp_1():
    clamp(15, 0, 10) == 10
    
def test_clamp_2():
    assert clamp(0, 0, 0) == 0