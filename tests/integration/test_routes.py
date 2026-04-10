import pytest
from src.pricing.routes import app
from src.database import reset_db


@pytest.fixture
def client():
    # preparation test client
    reset_db()
    with app.test_client() as client:
        yield client


# Tests pour POST /orders/simulate
def test_should_return_200_with_correct_total_when_order_is_valid(client):
    """1. Commande normale → 200 + detail correct"""
    payload = {
        "items": [{"name": "Pizza", "price": 10.0, "quantity": 2}],
        "distance": 5,
        "weight": 2,
        "promoCode": "",
        "hour": "15:00",
        "dayOfWeek": "Lundi",
    }
    response = client.post("/orders/simulate", json=payload)
    assert response.status_code == 200
    assert response.json["total"] == 23.0  # 20 (subtotal) + 3 (delivery)


def test_should_apply_discount_when_valid_promo_code_is_given(client):
    """2. Avec code promo valide → reduction appliquee"""
    payload = {
        "items": [{"name": "Pizza", "price": 25.0, "quantity": 2}],  # 50.0
        "distance": 5,
        "weight": 2,
        "promoCode": "BIENVENUE20",
        "hour": "15:00",
        "dayOfWeek": "Lundi",
    }
    response = client.post("/orders/simulate", json=payload)
    assert response.status_code == 200
    assert response.json["discount"] == 40  # 50 * 0.2
    assert response.json["total"] == 43.0  # (50-10) + 3


def test_should_return_400_when_simulating_with_expired_promo(client):
    """3. Avec code promo expired → 400 + message error"""
    payload = {
        "items": [{"name": "Pizza", "price": 25.0, "quantity": 2}],  # 50.0
        "distance": 5,
        "weight": 2,
        "promoCode": "TODAY30",
        "hour": "15:00",
        "dayOfWeek": "Lundi",
    }
    response = client.post("/orders/simulate", json=payload)
    assert response.status_code == 400
    assert "expired" in response.json["error"]


def test_should_return_400_when_items_are_empty(client):
    """4 Panier vide"""
    payload = {
        "items": [],
        "distance": 5,
        "weight": 2,
        "promoCode": "TODAY30",
        "hour": "15:00",
        "dayOfWeek": "Lundi",
    }
    response = client.post("/orders/simulate", json=payload)
    assert response.status_code == 400
    assert "empty" in response.json["error"]


def test_should_return_400_when_simulate_distance_exceeds_limit(client):
    """5 Hors zone (> 10 km) → 400"""
    payload = {
        "items": [{"name": "Pizza", "price": 25.0, "quantity": 2}],  # 50.0
        "distance": 15,
        "weight": 2,
        "promoCode": "",
        "hour": "15:00",
        "dayOfWeek": "Lundi",
    }
    response = client.post("/orders/simulate", json=payload)
    assert response.status_code == 400
    assert "refus" in response.json["error"]


def test_should_return_400_when_service_is_closed(client):
    """6 Ferme 22:00"""
    payload = {
        "items": [{"name": "Pizza", "price": 25.0, "quantity": 2}],
        "distance": 3,
        "weight": 2,
        "promoCode": "",
        "hour": "22:00",
        "dayOfWeek": "Lundi",
    }
    response = client.post("/orders/simulate", json=payload)
    assert response.status_code == 400
    assert "Hors de service" in response.json["error"]


def test_should_apply_surge_and_promo_when_friday_night_with_discount(client):
    """7. Surge (Vendredi 20h) + Promo -> Calcul combiné"""
    payload = {
        "items": [{"name": "Pizza", "price": 25.0, "quantity": 2}],  # 50.0
        "distance": 5,
        "weight": 2,
        "promoCode": "BIENVENUE20",
        "hour": "20:00",
        "dayOfWeek": "Vendredi",
    }
    response = client.post("/orders/simulate", json=payload)

    assert response.status_code == 200
    assert response.json["surge"] == 1.8
    assert response.json["deliveryFee"] == 5.4
    assert response.json["total"] == 45.4


# Tests pour POST /orders
def test_should_return_201_with_id_when_order_is_valid(client):
    """1. Commande valide → 201 + ID présent"""
    payload = {
        "items": [{"name": "Pizza", "price": 10.0, "quantity": 1}],
        "distance": 1,
        "weight": 1,
        "promoCode": "",
        "hour": "12:00",
        "dayOfWeek": "Lundi",
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["id"] == 1


def test_should_return_order_when_retrieved_by_existing_id(client):
    """2. Retrouvable via GET /orders/:id"""
    payload = {
        "items": [{"name": "A", "price": 10, "quantity": 1}],
        "distance": 1,
        "weight": 1,
        "hour": "12:00",
        "dayOfWeek": "Lundi",
    }
    post_res = client.post("/orders", json=payload)
    order_id = post_res.json["id"]

    get_res = client.get(f"/orders/{order_id}")
    assert get_res.status_code == 200
    assert get_res.json["id"] == order_id


def test_should_assign_different_ids_when_multiple_orders_created(client):
    """3. Deux commandes → deux IDs différents"""
    payload = {
        "items": [{"name": "A", "price": 10, "quantity": 1}],
        "distance": 1,
        "weight": 1,
        "hour": "12:00",
        "dayOfWeek": "Lundi",
    }
    res1 = client.post("/orders", json=payload)
    res2 = client.post("/orders", json=payload)

    assert res1.json["id"] != res2.json["id"]
    assert res1.json["id"] == 1
    assert res2.json["id"] == 2


def test_should_return_400_when_create_order_distance_exceeds_limit(client):
    """4. Commande invalide (ex: distance > 10km) → 400"""
    payload = {
        "items": [{"name": "Pizza", "price": 10.0, "quantity": 1}],
        "distance": 20,  # Trop loin
        "weight": 1,
        "hour": "12:00",
        "dayOfWeek": "Lundi",
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 400
    assert "refus" in response.json["error"]


def test_should_not_save_order_when_items_are_empty(client):
    """5. Vérifier que la commande invalide n'est PAS enregistrée"""
    payload = {
        "items": [],
        "distance": 1,
        "weight": 1,
        "hour": "12:00",
        "dayOfWeek": "Lundi",
    }  # Panier vide
    client.post("/orders", json=payload)  # Doit échouer
    # On vérifie que le GET sur l'ID 1 renvoie 404
    response = client.get("/orders/1")
    assert response.status_code == 404


# Tests pour GET /orders/:id
def test_should_return_200_with_order_data_when_id_exists(client):
    """1. ID existant → 200 + commande complète"""
    payload = {
        "items": [{"name": "Pizza", "price": 10.0, "quantity": 1}],
        "distance": 1,
        "weight": 1,
        "promoCode": "",
        "hour": "12:00",
        "dayOfWeek": "Lundi",
    }
    client.post("/orders", json=payload)

    response = client.get("/orders/1")

    assert response.status_code == 200
    assert response.json["id"] == 1
    assert "total" in response.json
    assert "items" in response.json


def test_should_return_404_when_order_id_not_found(client):
    """2. ID inexistant → 404"""
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert "error" in response.json


def test_should_return_complete_structure_when_order_is_retrieved(client):
    """3. La structure retournée est correcte"""
    payload = {
        "items": [{"name": "Test", "price": 5.0, "quantity": 1}],
        "distance": 1,
        "weight": 1,
        "hour": "12:00",
        "dayOfWeek": "Lundi",
    }
    client.post("/orders", json=payload)

    response = client.get("/orders/1")
    data = response.json

    required_keys = ["id", "items", "subtotal", "deliveryFee", "discount", "total"]
    for key in required_keys:
        assert key in data


# Test POST /promo/validate
def test_should_return_200_with_valid_status_when_promo_code_is_valid(client):
    """1. Code valide → 200 + détails"""
    payload = {
        "promoCode": "BIENVENUE20",
        "subtotal": 100,
        "current_date": "2026-04-09",
    }
    response = client.post("/promo/validate", json=payload)
    assert response.status_code == 200
    assert response.json["status"] == "valid"
    assert response.json["discount_amount"] == 80
    assert response.json["type"] == "percentage"


def test_should_return_400_when_validating_expired_promo_code(client):
    """2. Code expiré (TODAY30 expire le 08/04/2026) → 400"""
    payload = {
        "promoCode": "TODAY30",
        "subtotal": 100,
        "current_date": "2026-04-09",  # On est le 9, c'est trop tard
    }
    response = client.post("/promo/validate", json=payload)
    assert response.status_code == 400
    assert "expired" in response.json["error"]


def test_should_return_400_when_subtotal_is_below_minimum_order(client):
    """3. Commande sous le minimum (PROMO10 demande 30€) → 400"""
    payload = {
        "promoCode": "PROMO10",
        "subtotal": 20,  # 20 < 30
        "current_date": "2026-04-09",
    }
    response = client.post("/promo/validate", json=payload)
    assert response.status_code == 400
    assert "minOrder" in response.json["error"]


def test_should_return_404_when_promo_code_is_unknown(client):
    """4. Code inconnu → 404"""
    payload = {
        "promoCode": "FauxCode123",
        "subtotal": 100,
        "current_date": "2026-04-09",
    }
    response = client.post("/promo/validate", json=payload)
    assert response.status_code == 404
    assert response.json["error"] == "Code inconnu"


def test_should_return_400_when_promo_code_is_missing_from_body(client):
    """5. Sans code dans le body → 400"""
    payload = {
        "subtotal": 100  # Manque promoCode
    }
    response = client.post("/promo/validate", json=payload)
    assert response.status_code == 400
    assert "Missing" in response.json["error"]
