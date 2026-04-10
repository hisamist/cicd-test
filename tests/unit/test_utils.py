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
def test_should_return_titlecase_when_input_is_lowercase():
    assert capitalize("hello") == "Hello"


def test_should_return_titlecase_when_input_is_uppercase():
    assert capitalize("WORLD") == "World"


def test_should_return_empty_string_when_capitalize_receives_empty_input():
    assert capitalize("") == ""


def test_should_return_empty_string_when_capitalize_receives_none():
    assert capitalize(None) == ""


# Test Fonction 2:calculateAverage(numbers)
def test_should_return_average_when_given_multiple_positive_integers():
    assert calculateAverage([10, 12, 14]) == 12


def test_should_return_element_when_list_has_single_element():
    assert calculateAverage([15]) == 15


def test_should_return_zero_when_list_is_empty():
    assert calculateAverage([]) == 0


def test_should_return_rounded_average_when_result_is_not_exact():
    assert calculateAverage([10, 11, 12]) == 11


def test_should_return_zero_when_average_input_is_none():
    assert calculateAverage(None) == 0


# Test Fonction 3: slugify(text)
def test_should_return_kebabcase_when_input_is_normal_string():
    assert slugify("Hello World") == "hello-world"


def test_should_trim_whitespace_when_input_has_extra_spaces():
    assert slugify(" Spaces Everywhere ") == "spaces-everywhere"


def test_should_strip_accents_and_special_chars_when_input_has_them():
    assert slugify("C'est l'ete !") == "cest-lete"


def test_should_return_empty_string_when_slugify_receives_none():
    assert slugify(None) == ""


# Test Fonction 4: clamp(value, min, max)
def test_should_return_value_unchanged_when_within_boundaries():
    assert clamp(5, 0, 10) == 5


def test_should_return_minimum_when_value_is_below_range():
    assert clamp(-5, 0, 10) == 0


def test_should_return_maximum_when_value_is_above_range():
    assert clamp(15, 0, 10) == 10


def test_should_return_zero_when_min_and_max_are_zero():
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
def test_should_sort_ascending_when_sorted_by_grade_asc():
    result = sort_students(students, "grade", "asc")
    assert result[0]["grade"] == 12
    assert result[1]["grade"] == 15
    assert result[2]["grade"] == 18


# 2. should sort students by grade descending
def test_should_sort_descending_when_sorted_by_grade_desc():
    result = sort_students(students, "grade", "desc")
    assert result[0]["grade"] == 18
    assert result[1]["grade"] == 15
    assert result[2]["grade"] == 12


# 3. should sort students by name ascending
def test_should_sort_alphabetically_when_sorted_by_name_asc():
    result = sort_students(students, "name", "asc")
    assert result[0]["name"] == "Alice"
    assert result[1]["name"] == "Bob"
    assert result[2]["name"] == "Charlie"


# 4. should sort students by age ascending
def test_should_sort_by_age_ascending_when_order_is_asc():
    result = sort_students(students, "age", "asc")
    assert result[0]["age"] == 19
    assert result[1]["age"] == 20
    assert result[2]["age"] == 22


# 5. should return empty array for null input
def test_should_return_empty_array_when_students_input_is_null():
    result = sort_students(None, "age", "asc")
    assert len(result) == 0


# 6. should return empty array for empty input
def test_should_return_empty_array_when_students_input_is_empty():
    result = sort_students([], "age", "asc")
    assert len(result) == 0


# 7. should not modify the original array
def test_should_not_modify_original_array_when_sorting():
    # copy original
    import copy

    original_students = copy.deepcopy(students)
    sort_students(students, "age", "asc")

    assert students == original_students


# 8. should default to ascending order
def test_should_sort_ascending_by_default_when_no_order_given():
    result = sort_students(students, "age")
    assert result[0]["age"] == 19
    assert result[1]["age"] == 20
    assert result[2]["age"] == 22


# Test Fonction parse Price
def test_should_return_none_when_parse_price_input_is_null():
    assert parse_price(None) is None


def test_should_return_none_when_price_is_negative():
    assert parse_price("-5") is None


def test_should_return_float_when_price_uses_dot_separator():
    assert parse_price("12.99") == 12.99


def test_should_return_float_when_price_uses_comma_separator():
    assert parse_price("12,99") == 12.99


def test_should_return_float_when_price_has_euro_suffix():
    assert parse_price("12,99 €") == 12.99


def test_should_return_float_when_price_has_euro_prefix():
    assert parse_price("€12.99") == 12.99


def test_should_return_float_when_price_has_extra_text():
    assert parse_price("12.99 (nombre)") == 12.99


def test_should_return_zero_when_price_string_is_gratuit():
    assert parse_price("gratuit") == 0


def test_should_return_none_when_price_string_is_invalid_text():
    assert parse_price("abc") is None


# Test 6 groupBy(array, key)
GROUP = [
    {"name": "Alice", "role": "dev"},
    {"name": "Bob", "role": "design"},
    {"name": "Charlie", "role": "dev"},
]


def test_should_raise_error_when_group_by_receives_empty_array():
    with pytest.raises(ValueError, match="input required"):
        assert group_by([], "role")


def test_should_raise_error_when_group_by_receives_null_members():
    with pytest.raises(ValueError, match="input required"):
        assert group_by(None, "role")


def test_should_raise_error_when_group_by_receives_null_key():
    with pytest.raises(ValueError, match="input required"):
        assert group_by(GROUP, None)


def test_should_raise_error_when_key_does_not_match_any_field():
    with pytest.raises(ValueError, match="unmatch key"):
        assert group_by(GROUP, "class")


def test_should_return_grouped_dict_when_key_matches_field():
    result = group_by(GROUP, "role")
    expected_result = {"dev": ["Alice", "Charlie"], "design": ["Bob"]}
    assert result == expected_result


def test_should_return_single_group_when_all_members_share_same_key():
    GROUP = [{"name": "Alice", "role": "dev"}, {"name": "Charlie", "role": "dev"}]
    expected = {"dev": ["Alice", "Charlie"]}
    assert group_by(GROUP, "role") == expected


# Test7 calculate discount(price, discountRules)
def test_should_raise_error_when_price_is_none():
    with pytest.raises(ValueError, match="price required"):
        assert calculate_discount(None, [{"type": "percentage", "value": 10}])


def test_should_return_original_price_when_rules_are_empty():
    assert calculate_discount(100, []) == 100


def test_should_apply_percentage_discount_when_rule_type_is_percentage():
    assert calculate_discount(100, [{"type": "percentage", "value": 10}]) == 90


def test_should_apply_fixed_discount_when_rule_type_is_fixed():
    assert calculate_discount(100, [{"type": "fixed", "value": 5}]) == 95


def test_should_apply_combined_discounts_when_multiple_rules_given():
    assert (
        calculate_discount(
            100, [{"type": "percentage", "value": 10}, {"type": "fixed", "value": 5}]
        )
        == 85
    )


def test_should_give_free_item_when_rule_type_is_buyxgety():
    # Acheter 4 articles à 10€ chacun, obtenir 1 gratuit
    # 4 articles => 3 payants et 1 gratuit => total de réduction = 10€
    result = calculate_discount(
        40, [{"type": "buyxgety", "buy": 3, "free": 1, "itemPrice": 10}]
    )
    assert result == 30  # 40€ - 10€ = 30€


def test_should_return_zero_when_discount_exceeds_price():
    assert calculate_discount(10, [{"type": "fixed", "value": 15}]) == 0
