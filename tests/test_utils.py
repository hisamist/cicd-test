from src.utils import capitalize
from src.utils import calculateAverage
from src.utils import slugify
from src.utils import clamp

# Test Fonction 1 : capitalize
def test_capilize_converts_lowercase_to_titlecase():
    assert capitalize("hello") == "Hello"

def test_capitalize_converts_uppercase_to_titlecase():
    assert capitalize("WORLD") == "World"

def test_capitalize_returns_empty_string_for_empty_imput():
    assert capitalize("") == ""

def test_capitalize_handles_none_input():
    assert capitalize(None)== ""

# Test Fonction 2:calculateAverage(numbers)
def test_calculate_average_of_multiple_positive_integers():
    assert calculateAverage([10,12,14]) == 12

def test_calculate_average_single_element_list():
    assert calculateAverage([15]) == 15

def test_calculate_average_returns_zero_for_empty_list():
    assert calculateAverage([]) == 0

def test_calculate_average_of_multiple_positive_list_rounding():
    assert calculateAverage([10,11,12]) == 11

def test_calculate_average_returns_zero_for_none_input():
    assert calculateAverage(None)== 0

# Test Fonction 3: slugify(text)
def test_slugify_converts_string_to_kebabcase():
    assert slugify("Hello World") =="hello-world"

def test_slugify_trims_unnecessary_whitespace():
    assert slugify(" Spaces Everywhere ") =="spaces-everywhere"

def test_slugify_strips_accents_and_special_characters():
    assert slugify("C'est l'ete !") =="cest-lete"

def test_slugify_handles_none_by_returning_empty_string():
    assert slugify(None) == ""

# Test Fonction 4: clamp(value, min, max)
def test_clamp_keeps_value_within_boundaries():
    assert clamp(5, 0, 10) == 5

def test_clamp_forces_minimum_value_when_below_range():
    assert clamp(-5, 0, 10) == 0

def test_clamp_forces_maximum_value_when_above_range():
    clamp(15, 0, 10) == 10
    
def test_clamp_handles_zero_range_correctly():
    assert clamp(0, 0, 0) == 0