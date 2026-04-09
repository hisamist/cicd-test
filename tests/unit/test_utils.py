from src.exercise.utils import capitalize
from src.exercise.utils import calculateAverage
from src.exercise.utils import slugify
from src.exercise.utils import clamp
from src.exercise.utils import sort_students
from src.exercise.utils import parse_price
from src.exercise.utils import group_by
from src.exercise.utils import calculate_discount
import pytest


# Test Fonction 1 : capitalize
def test_capilize_converts_lowercase_to_titlecase():
    assert capitalize("hello") == "Hello"


def test_capitalize_converts_uppercase_to_titlecase():
    assert capitalize("WORLD") == "World"


def test_capitalize_returns_empty_string_for_empty_imput():
    assert capitalize("") == ""


def test_capitalize_handles_none_input():
    assert capitalize(None) == ""


# Test Fonction 2:calculateAverage(numbers)
def test_calculate_average_of_multiple_positive_integers():
    assert calculateAverage([10, 12, 14]) == 12


def test_calculate_average_single_element_list():
    assert calculateAverage([15]) == 15


def test_calculate_average_returns_zero_for_empty_list():
    assert calculateAverage([]) == 0


def test_calculate_average_of_multiple_positive_list_rounding():
    assert calculateAverage([10, 11, 12]) == 11


def test_calculate_average_returns_zero_for_none_input():
    assert calculateAverage(None) == 0


# Test Fonction 3: slugify(text)
def test_slugify_converts_string_to_kebabcase():
    assert slugify("Hello World") == "hello-world"


def test_slugify_trims_unnecessary_whitespace():
    assert slugify(" Spaces Everywhere ") == "spaces-everywhere"


def test_slugify_strips_accents_and_special_characters():
    assert slugify("C'est l'ete !") == "cest-lete"


def test_slugify_handles_none_by_returning_empty_string():
    assert slugify(None) == ""


# Test Fonction 4: clamp(value, min, max)
def test_clamp_keeps_value_within_boundaries():
    assert clamp(5, 0, 10) == 5


def test_clamp_forces_minimum_value_when_below_range():
    assert clamp(-5, 0, 10) == 0


def test_clamp_forces_maximum_value_when_above_range():
    assert clamp(15, 0, 10) == 10


def test_clamp_handles_zero_range_correctly():
    assert clamp(0, 0, 0) == 0


# sort students
students = [
    {"name": "Charlie", "grade": 12, "age": 20},
    {"name": "Alice", "grade": 18, "age": 22},
    {"name": "Bob", "grade": 15, "age": 19},
]

# sort students
students = [
    {"name": "Charlie", "grade": 12, "age": 20},
    {"name": "Alice", "grade": 18, "age": 22},
    {"name": "Bob", "grade": 15, "age": 19},
]


# 1. should sort students by grade ascending
def test_sort_students_by_grade_asc():
    result = sort_students(students, "grade", "asc")
    assert result[0]["grade"] == 12
    assert result[1]["grade"] == 15
    assert result[2]["grade"] == 18


# 2. should sort students by grade descending
def test_sort_students_by_grade_desc():
    result = sort_students(students, "grade", "desc")
    assert result[0]["grade"] == 18
    assert result[1]["grade"] == 15
    assert result[2]["grade"] == 12


# 3. should sort students by name ascending
def test_sort_students_by_name_asc():
    result = sort_students(students, "name", "asc")
    assert result[0]["name"] == "Alice"
    assert result[1]["name"] == "Bob"
    assert result[2]["name"] == "Charlie"


# 4. should sort students by age ascending
def test_sort_students_by_age_asc():
    result = sort_students(students, "age", "asc")
    assert result[0]["age"] == 19
    assert result[1]["age"] == 20
    assert result[2]["age"] == 22


# 5. should return empty array for null input
def test_sort_students_send_empty_array_for_null_imput():
    result = sort_students(None, "age", "asc")
    assert len(result) == 0


# 6. should return empty array for empty input
def test_sort_students_send_empty_array_for_empty_imput():
    result = sort_students([], "age", "asc")
    assert len(result) == 0


# 7. should not modify the original array
def test_sort_students_does_not_modify_original():
    # copy original
    import copy

    original_students = copy.deepcopy(students)
    sort_students(students, "age", "asc")

    assert students == original_students


# 8. should default to ascending order
def test_sort_students_send_array_asc_as_default():
    result = sort_students(students, "age")
    assert result[0]["age"] == 19
    assert result[1]["age"] == 20
    assert result[2]["age"] == 22


# Test Fonction parse Price
def test_parse_price_send_null_for_null_imput():
    assert parse_price(None) is None


def test_parse_price_send_null_for_negative_imput():
    assert parse_price("-5") is None


def test_parse_price_send_positive_numbers_dot():
    assert parse_price("12.99") == 12.99


def test_parse_price_send_positive_numbers_comma():
    assert parse_price("12,99") == 12.99


def test_parse_price_send_positive_numbers_for_with_euro_suffix():
    assert parse_price("12,99 €") == 12.99


def test_parse_price_send_positive_numbers_for_with_euro_prefix():
    assert parse_price("€12.99") == 12.99


def test_parse_price_send_positive_numbers_for_with_extra_text():
    assert parse_price("12.99 (nombre)") == 12.99


def test_parse_price_send_zero_for_free_str():
    assert parse_price("gratuit") == 0


def test_parse_price_send_null_for_invalid_text():
    assert parse_price("abc") is None


# Test 6 groupBy(array, key)
GROUP = [
    {"name": "Alice", "role": "dev"},
    {"name": "Bob", "role": "design"},
    {"name": "Charlie", "role": "dev"},
]


def test_group_by_with_empty_array():
    with pytest.raises(ValueError, match="input required"):
        assert group_by([], "role")


def test_group_by_with_null_members():
    with pytest.raises(ValueError, match="input required"):
        assert group_by(None, "role")


def test_group_by_with_null_role():
    with pytest.raises(ValueError, match="input required"):
        assert group_by(GROUP, None)


def test_group_by_error_with_unmatched_key():
    with pytest.raises(ValueError, match="unmatch key"):
        assert group_by(GROUP, "class")


def test_group_send_sorted_result_by_key():
    result = group_by(GROUP, "role")
    expected_result = {"dev": ["Alice", "Charlie"], "design": ["Bob"]}
    assert result == expected_result


def test_group_by_single_group():
    GROUP = [{"name": "Alice", "role": "dev"}, {"name": "Charlie", "role": "dev"}]
    expected = {"dev": ["Alice", "Charlie"]}
    assert group_by(GROUP, "role") == expected


# Test7 calculate discount(price, discountRules)
def test_calculate_discount_error_for_empty_price():
    with pytest.raises(ValueError, match="price required"):
        assert calculate_discount(None, [{"type": "percentage", "value": 10}])


def test_calculate_discount_send_original_price_for_empty_rules():
    assert calculate_discount(100, []) == 100


def test_calculate_discount_success_with_percentage_type():
    assert calculate_discount(100, [{"type": "percentage", "value": 10}]) == 90


def test_calculate_discount_success_with_fixed_type():
    assert calculate_discount(100, [{"type": "fixed", "value": 5}]) == 95


def test_calculate_discount_success_with_fixed_type_and_percentage_type():
    assert (
        calculate_discount(
            100, [{"type": "percentage", "value": 10}, {"type": "fixed", "value": 5}]
        )
        == 85
    )


def test_buyXgetY_discount_4_items():
    # Acheter 4 articles à 10€ chacun, obtenir 1 gratuit
    # 4 articles => 3 payants et 1 gratuit => total de réduction = 10€
    result = calculate_discount(
        40, [{"type": "buyxgety", "buy": 3, "free": 1, "itemPrice": 10}]
    )
    assert result == 30  # 40€ - 10€ = 30€


def test_calculate_discount_send_zero_for_nagative_result():
    assert calculate_discount(10, [{"type": "fixed", "value": 15}]) == 0
