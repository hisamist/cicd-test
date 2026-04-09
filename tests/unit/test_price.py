import pytest
from src.pricing.price import calculate_delivery_fee
from src.pricing.price import apply_promo_code
from src.pricing.price import calculate_surge
from src.pricing.price import calculate_order_total
from src.database import PROMO_CODES


# Fonction 1: calculate_delivery_fee
def test_calculate_delivery_fee_without_additional_fee():
    result = calculate_delivery_fee(2, 1)
    assert result == 2


def test_calculate_delivery_fee_with_border_distance():
    result = calculate_delivery_fee(3, 1)
    assert result == 2


def test_calculate_delivery_fee_with_additional_delivery_fee_for_4km():
    result = calculate_delivery_fee(4, 1)
    assert result == 2.5


def test_calculate_delivery_fee_with_additional_delivery_fee_for_6km():
    result = calculate_delivery_fee(6, 1)
    assert result == 3.5


def test_calculate_delivery_fee_with_additional_delivery_fee_for_():
    result = calculate_delivery_fee(9.6, 1)
    assert result == 5.5


def test_calculate_delivery_fee_refuses_long_distance_sending_error():
    # More than 10 km
    # ValueError with message "refuse"
    with pytest.raises(ValueError, match="refuse"):
        calculate_delivery_fee(10, 5)


def test_calculate_delivery_fee_with_base_distance_and_border_weight():
    result = calculate_delivery_fee(2, 5)
    assert result == 3.5


def test_calculate_delivery_fee_with_base_distance_and_above_border_weight():
    result = calculate_delivery_fee(2, 6)
    assert result == 3.5


def test_calculate_delivery_fee_with_negative_distance_sending_error():
    with pytest.raises(ValueError, match="negative"):
        calculate_delivery_fee(-2, 6)


def test_calculate_delivery_fee_with_negative_weight_sending_error():
    with pytest.raises(ValueError, match="negative"):
        calculate_delivery_fee(2, -2)


def test_calculate_delivery_fee_with_zero_distance_sending_error():
    with pytest.raises(ValueError, match="negative"):
        calculate_delivery_fee(0, 2)


def test_calculate_delivery_fee_with_zero_weight_sending_error():
    with pytest.raises(ValueError, match="negative"):
        calculate_delivery_fee(3, 0)


# Fonction 2 : apply_promo_code


#  Cas normaux
def test_apply_promo_code_percentage_success():
    # 2O% off from 50 euros with correct promo code
    assert apply_promo_code(50, "BIENVENUE20", PROMO_CODES) == 40


def test_apply_promo_code_fixed_success():
    # 5 euros off with correct promo code
    assert apply_promo_code(30, "PROMO5", PROMO_CODES) == 25


# Refus du code
def test_apply_promo_code_refused_because_of_expiration_date():
    with pytest.raises(ValueError, match="code expired"):
        apply_promo_code(40, "TODAY30", PROMO_CODES)


def test_apply_promo_code_subtotal_is_smaller_than_minOrder_error():
    # Code valide avec minOrder respecte
    with pytest.raises(ValueError, match="minOrder not met"):
        apply_promo_code(20, "PROMO10", PROMO_CODES)


def test_apply_promo_code_refused_because_of_invalid_code():
    with pytest.raises(ValueError, match="invalid code"):
        apply_promo_code(40, "PROMO????", PROMO_CODES)


def test_apply_promo_prevent_negative_total():
    assert apply_promo_code(5, "PROMOMO", PROMO_CODES) == 0


def test_apply_promo_works_on_expiry_day():
    assert apply_promo_code(40, "TODAY30", PROMO_CODES, "2026-04-08") == 30


# Entrees invalides
def test_apply_promo_code_without_reduction_for_code_null():
    assert apply_promo_code(120, None, PROMO_CODES) == 120


def test_apply_promo_code_without_reduction_for_empty_code():
    assert apply_promo_code(120, "", PROMO_CODES) == 120


def test_apply_promo_code_send_error_for_subtotal_negative():
    with pytest.raises(ValueError, match="negative"):
        apply_promo_code(-120, "", PROMO_CODES)


# Test Fonction 3 : calculateSurge(hour, dayOfWeek)
def test_calculate_surge_send_normal_rate():
    assert calculate_surge("15:00", "Mardi") == 1


def test_calculate_surge_send_weekday_noon_rate():
    assert calculate_surge("12:30", "Mercredi") == 1.3


def test_calculate_surge_send_weekday_evening_rate():
    assert calculate_surge("20:00", "Jeudi") == 1.5


def test_calculate_surge_send_weekend_evening_rate():
    assert calculate_surge("21:00", "Vendredi") == 1.8


def test_calculate_surge_send_sunday_rate():
    assert calculate_surge("14:00", "Dimanche") == 1.2


def test_calculate_surge_send_close_rate():
    assert calculate_surge("09:59", "Dimanche") == 0


def test_calculate_surge_send_rate_by_border_open_hour():
    assert calculate_surge("10:00", "Dimanche") == 1.2


def test_calculate_surge_send_rate_by_border_close_hour():
    assert calculate_surge("22:01", "Dimanche") == 0


def test_calculate_surge_send_error_for_empty_params():
    with pytest.raises(ValueError, match="manque params"):
        calculate_surge("", "")


# Test Fonction4: Calculate Order Total
TEST_DATE = "2026-04-09"


def test_calculate_order_total_success():
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


def test_calculate_order_total_success_with_20pourcent_discount():
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


def test_calculate_order_total_success_with_fix_discount():
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


def test_calculate_order_total_success_with_surge_for_friday_night():
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


def test_calculate_order_total_success_with_surge_for_friday_night_with_discount():
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


def test_calculate_order_total_send_error_for_empty_items():
    with pytest.raises(ValueError, match="empty items"):
        calculate_order_total([], 1, 2, "PROMO5", "16:00", "Mercredi", TEST_DATE)


def test_calculate_order_total_send_error_for_items_price_zero():
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


def test_calculate_order_total_send_error_for_negative_price_of_item():
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


def test_calculate_order_total_send_error_for_out_of_service():
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


def test_calculate_order_total_send_error_for_distance_limit():
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


def test_calculate_order_total_send_error_for_expiration_code():
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
