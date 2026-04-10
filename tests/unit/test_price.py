import pytest
from src.pricing.price import calculate_delivery_fee
from src.pricing.price import apply_promo_code
from src.pricing.price import calculate_surge
from src.pricing.price import calculate_order_total
from src.database import PROMO_CODES


# Fonction 1: calculate_delivery_fee
def test_should_return_base_fee_when_distance_is_within_base_range():
    result = calculate_delivery_fee(2, 1)
    assert result == 2


def test_should_return_base_fee_when_distance_is_at_border():
    result = calculate_delivery_fee(3, 1)
    assert result == 2


def test_should_add_extra_fee_when_distance_is_4km():
    result = calculate_delivery_fee(4, 1)
    assert result == 2.5


def test_should_add_extra_fee_when_distance_is_6km():
    result = calculate_delivery_fee(6, 1)
    assert result == 3.5


def test_should_add_extra_fee_when_distance_is_9_6km():
    result = calculate_delivery_fee(9.6, 1)
    assert result == 5.5


def test_should_raise_error_when_delivery_distance_exceeds_limit():
    # More than 10 km
    # ValueError with message "refuse"
    with pytest.raises(ValueError, match="refuse"):
        calculate_delivery_fee(10, 5)


def test_should_add_weight_fee_when_weight_is_at_border():
    result = calculate_delivery_fee(2, 5)
    assert result == 3.5


def test_should_add_weight_fee_when_weight_is_above_border():
    result = calculate_delivery_fee(2, 6)
    assert result == 3.5


def test_should_raise_error_when_distance_is_negative():
    with pytest.raises(ValueError, match="negative"):
        calculate_delivery_fee(-2, 6)


def test_should_raise_error_when_weight_is_negative():
    with pytest.raises(ValueError, match="negative"):
        calculate_delivery_fee(2, -2)


def test_should_raise_error_when_distance_is_zero():
    with pytest.raises(ValueError, match="negative"):
        calculate_delivery_fee(0, 2)


def test_should_raise_error_when_weight_is_zero():
    with pytest.raises(ValueError, match="negative"):
        calculate_delivery_fee(3, 0)


# Fonction 2 : apply_promo_code


#  Cas normaux
def test_should_apply_percentage_discount_when_promo_code_is_percentage_type():
    # 2O% off from 50 euros with correct promo code
    assert apply_promo_code(50, "BIENVENUE20", PROMO_CODES) == 40


def test_should_apply_fixed_discount_when_promo_code_is_fixed_type():
    # 5 euros off with correct promo code
    assert apply_promo_code(30, "PROMO5", PROMO_CODES) == 25


# Refus du code
def test_should_raise_error_when_promo_code_is_expired():
    with pytest.raises(ValueError, match="code expired"):
        apply_promo_code(40, "TODAY30", PROMO_CODES)


def test_should_raise_error_when_subtotal_is_below_min_order():
    # Code valide avec minOrder respecte
    with pytest.raises(ValueError, match="minOrder not met"):
        apply_promo_code(20, "PROMO10", PROMO_CODES)


def test_should_raise_error_when_promo_code_is_invalid():
    with pytest.raises(ValueError, match="invalid code"):
        apply_promo_code(40, "PROMO????", PROMO_CODES)


def test_should_return_zero_when_discount_exceeds_subtotal():
    assert apply_promo_code(5, "PROMOMO", PROMO_CODES) == 0


def test_should_apply_discount_when_used_on_expiry_day():
    assert apply_promo_code(40, "TODAY30", PROMO_CODES, "2026-04-08") == 30


# Entrees invalides
def test_should_return_original_price_when_promo_code_is_null():
    assert apply_promo_code(120, None, PROMO_CODES) == 120


def test_should_return_original_price_when_promo_code_is_empty():
    assert apply_promo_code(120, "", PROMO_CODES) == 120


def test_should_raise_error_when_subtotal_is_negative():
    with pytest.raises(ValueError, match="negative"):
        apply_promo_code(-120, "", PROMO_CODES)


# Test Fonction 3 : calculateSurge(hour, dayOfWeek)
def test_should_return_normal_rate_when_time_is_off_peak():
    assert calculate_surge("15:00", "Mardi") == 1


def test_should_return_noon_rate_when_time_is_midday_on_weekday():
    assert calculate_surge("12:30", "Mercredi") == 1.3


def test_should_return_evening_rate_when_time_is_evening_on_weekday():
    assert calculate_surge("20:00", "Jeudi") == 1.5


def test_should_return_weekend_evening_rate_when_time_is_friday_night():
    assert calculate_surge("21:00", "Vendredi") == 1.8


def test_should_return_sunday_rate_when_day_is_sunday():
    assert calculate_surge("14:00", "Dimanche") == 1.2


def test_should_return_zero_rate_when_service_is_closed():
    assert calculate_surge("09:59", "Dimanche") == 0


def test_should_return_rate_when_time_is_at_opening_hour():
    assert calculate_surge("10:00", "Dimanche") == 1.2


def test_should_return_zero_when_time_is_after_closing_hour():
    assert calculate_surge("22:01", "Dimanche") == 0


def test_should_raise_error_when_params_are_empty():
    with pytest.raises(ValueError, match="manque params"):
        calculate_surge("", "")


# Test Fonction4: Calculate Order Total
TEST_DATE = "2026-04-09"


def test_should_return_correct_total_when_no_promo_code_given():
    # 2 pizzas a 12.50€ + 5 km + mardi 15h without discount
    result = calculate_order_total(
        [{"name": "Pizza", "price": 12.50, "quantity": 2}],
        5,
        2,
        "",
        "15:00",
        "Mercredi",
        TEST_DATE,
    )
    assert result["subtotal"] == 25
    assert result["discount"] == 25
    assert result["deliveryFee"] == 3
    assert result["surge"] == 1.0
    assert result["total"] == 28


def test_should_apply_percentage_promo_when_code_is_bienvenue20():
    # 2 pizzas a 20€ + 5 km + mardi 15h without discount 20 perrcent coupon
    result = calculate_order_total(
        [{"name": "Pizza", "price": 20, "quantity": 2}],
        5,
        2,
        "BIENVENUE20",
        "15:00",
        "Mercredi",
        TEST_DATE,
    )
    assert result["subtotal"] == 40
    assert result["discount"] == 32  # 20 percents off
    assert result["deliveryFee"] == 3
    assert result["surge"] == 1.0
    assert result["total"] == 35


def test_should_apply_fixed_promo_when_code_is_promo10():
    # 2 pizzas a 20€ + 5 km + mardi 15h without discount 20 perrcent coupon
    result = calculate_order_total(
        [{"name": "Pizza", "price": 20, "quantity": 2}],
        5,
        2,
        "PROMO10",
        "15:00",
        "Mercredi",
        TEST_DATE,
    )
    assert result["subtotal"] == 40
    assert result["discount"] == 30  # 10 euros moins
    assert result["deliveryFee"] == 3
    assert result["surge"] == 1.0
    assert result["total"] == 33


def test_should_apply_surge_multiplier_when_day_is_friday_night():
    # 2 pizzas a 12.50€ + 5 km + vendredi 20h
    result = calculate_order_total(
        [{"name": "Pizza", "price": 20, "quantity": 2}],
        5,
        2,
        "",
        "20:00",
        "Vendredi",
        TEST_DATE,
    )
    assert result["subtotal"] == 40
    assert result["discount"] == 40
    assert result["surge"] == 1.8
    assert result["deliveryFee"] == 5.4
    assert result["total"] == 45.4


def test_should_combine_surge_and_discount_when_friday_night_with_promo():
    # 2 pizzas a 12.50€ + 5 km + vendredi 20h + discount fix 10 euros
    result = calculate_order_total(
        [{"name": "Pizza", "price": 20, "quantity": 2}],
        5,
        2,
        "PROMO10",
        "20:00",
        "Vendredi",
        TEST_DATE,
    )
    assert result["subtotal"] == 40
    assert result["discount"] == 30
    assert result["surge"] == 1.8
    assert result["deliveryFee"] == 5.4
    assert result["total"] == 35.4


def test_should_raise_error_when_items_are_empty():
    with pytest.raises(ValueError, match="empty items"):
        calculate_order_total([], 1, 2, "PROMO5", "16:00", "Mercredi", TEST_DATE)


def test_should_raise_error_when_item_price_is_zero():
    with pytest.raises(ValueError, match="Le prix est inadequate"):
        calculate_order_total(
            [{"name": "Pizza", "price": 0, "quantity": 2}],
            1,
            2,
            "PROMO5",
            "16:00",
            "Mercredi",
            TEST_DATE,
        )


def test_should_raise_error_when_item_price_is_negative():
    with pytest.raises(ValueError, match="Le prix est inadequate"):
        calculate_order_total(
            [{"name": "Pizza", "price": -10, "quantity": 2}],
            1,
            2,
            "PROMO5",
            "16:00",
            "Mercredi",
            TEST_DATE,
        )


def test_should_raise_error_when_time_is_out_of_service():
    with pytest.raises(ValueError, match="Hors de service"):
        calculate_order_total(
            [{"name": "Pizza", "price": 20, "quantity": 2}],
            1,
            2,
            "PROMO5",
            "23:00",
            "Mercredi",
            TEST_DATE,
        )


def test_should_raise_error_when_order_distance_exceeds_limit():
    # Over 15 km
    with pytest.raises(ValueError, match="refuse"):
        calculate_order_total(
            [{"name": "Pizza", "price": 20, "quantity": 2}],
            15,
            2,
            "PROMO5",
            "16:00",
            "Mercredi",
            TEST_DATE,
        )


def test_should_raise_error_when_order_promo_code_is_expired():
    # code expired
    with pytest.raises(ValueError, match="code expired"):
        calculate_order_total(
            [{"name": "Pizza", "price": 20, "quantity": 2}],
            15,
            2,
            "PROMO5",
            "16:00",
            "Mercredi",
            "2027-12-31",
        )
