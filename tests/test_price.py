import pytest
from src.price import calculate_delivery_fee
from src.price import apply_promo_code
from datetime import datetime

# Fonction 1: calculate_delivery_fee
def test_calculate_delivery_fee_without_additional_fee():
    result = calculate_delivery_fee(2,1)
    assert result == 2 

def test_calculate_delivery_fee_with_border_distance():
    result = calculate_delivery_fee(3,1)
    assert result == 2 

def test_calculate_delivery_fee_with_additional_delivery_fee_for_4km():
    result = calculate_delivery_fee(4,1)
    assert result == 2.5

def test_calculate_delivery_fee_with_additional_delivery_fee_for_6km():
    result = calculate_delivery_fee(6,1)
    assert result == 3.5

def test_calculate_delivery_fee_with_additional_delivery_fee_for_():
    result = calculate_delivery_fee(9.6,1)
    assert result == 5.5

def test_calculate_delivery_fee_refuses_long_distance_sending_error():
    # More than 10 km 
    # ValueError with message "refuse"
    with pytest.raises(ValueError, match="refuse"):
        calculate_delivery_fee(10, 5)

def test_calculate_delivery_fee_with_base_distance_and_border_weight():
    result = calculate_delivery_fee(2,5)
    assert result == 3.5

def test_calculate_delivery_fee_with_base_distance_and_above_border_weight():
    result = calculate_delivery_fee(2,6)
    assert result == 3.5

def test_calculate_delivery_fee_with_negative_distance_sending_error():
    with pytest.raises(ValueError, match="negative"):
       calculate_delivery_fee(-2,6)

def test_calculate_delivery_fee_with_negative_weight_sending_error():
    with pytest.raises(ValueError, match="negative"):
       calculate_delivery_fee(2,-2)
  
def test_calculate_delivery_fee_with_zero_distance_sending_error():
    with pytest.raises(ValueError, match="negative"):
       calculate_delivery_fee(0,2)

def test_calculate_delivery_fee_with_zero_weight_sending_error():
    with pytest.raises(ValueError, match="negative"):
       calculate_delivery_fee(3,0)

# Fonction 2 : apply_promo_code
PROMO_CODES = [
    {
        "code": "BIENVENUE20",
        "type": "percentage",
        "value": 20,
        "minOrder": 15.00,
        "expiresAt": "2026-12-31"
    },
    {
        "code": "PROMO5",
        "type": "fixed",
        "value": 5,
        "minOrder": 10.00,
        "expiresAt": "2026-12-31"
    },
     {
        "code": "PROMO10",
        "type": "fixed",
        "value": 10,
        "minOrder": 30.00,
        "expiresAt": "2025-12-31"
    },

    {
        "code": "PROMOMO",
        "type": "fixed",
        "value": 10,
        "minOrder": 0,
        "expiresAt":"2026-04-08"
    },
    {
        "code": "TODAY30",
        "type": "fixed",
        "value": 10,
        "minOrder": 0,
        "expiresAt": "2026-04-08"
    },
]

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
       apply_promo_code(40,"PROMO10",PROMO_CODES)

def test_apply_promo_code_subtotal_is_smaller_than_minOrder_error():
   # Code valide avec minOrder respecte
    with pytest.raises(ValueError, match="minOrder not met"):
       apply_promo_code(20,"PROMO10",PROMO_CODES)

def test_apply_promo_code_refused_because_of_invalid_code():
    with pytest.raises(ValueError, match="invalid code"):
       apply_promo_code(40,"PROMO????",PROMO_CODES)

def test_apply_promo_prevent_negative_total():
    assert apply_promo_code(5,"PROMOMO",PROMO_CODES) == 0

def test_apply_promo_works_on_expiry_day():
    assert apply_promo_code(40,"TODAY30",PROMO_CODES,"2026-04-08") == 30

# Entrees invalides
def test_apply_promo_code_without_reduction_for_code_null():
    assert apply_promo_code(120,None,PROMO_CODES) == 120

def test_apply_promo_code_without_reduction_for_empty_code():
    assert apply_promo_code(120,"",PROMO_CODES) == 120

def test_apply_promo_code_send_error_for_subtotal_negative():
    with pytest.raises(ValueError, match="negative"):
       apply_promo_code(-120,"",PROMO_CODES)
    