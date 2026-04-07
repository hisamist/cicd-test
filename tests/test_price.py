import pytest
from src.price import calculate_delivery_fee

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