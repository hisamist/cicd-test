import pytest
from src.routes import app
from src.database import reset_db


@pytest.fixture
def client():
    # preparation test client
    reset_db()
    with app.test_client() as client:
        yield client


# Tests pour POST /orders/simulate
def test_simulate_normal_order(client):
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


def test_simulate_with_promo(client):
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


def test_simulate_error_with_promo_expired(client):
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


def test_simulate_error_with_empty_items(client):
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


def test_simulate_error_with_above_distance_limit(client):
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


def test_simulate_error_with_close_service(client):
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


def test_simulate_with_multiplied_price(client):
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
def test_create_order_success(client):
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


def test_order_is_retrievable(client):
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


def test_multiple_orders_different_ids(client):
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


def test_create_order_invalid(client):
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


def test_invalid_order_not_saved(client):
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
def test_get_order_by_id_exists(client):
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


def test_get_order_by_id_not_found(client):
    """2. ID inexistant → 404"""
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert "error" in response.json


def test_get_order_payload_structure(client):
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
def test_promo_valid(client):
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


def test_promo_expired(client):
    """2. Code expiré (TODAY30 expire le 08/04/2026) → 400"""
    payload = {
        "promoCode": "TODAY30",
        "subtotal": 100,
        "current_date": "2026-04-09",  # On est le 9, c'est trop tard
    }
    response = client.post("/promo/validate", json=payload)
    assert response.status_code == 400
    assert "expired" in response.json["error"]


def test_promo_min_order_not_met(client):
    """3. Commande sous le minimum (PROMO10 demande 30€) → 400"""
    payload = {
        "promoCode": "PROMO10",
        "subtotal": 20,  # 20 < 30
        "current_date": "2026-04-09",
    }
    response = client.post("/promo/validate", json=payload)
    assert response.status_code == 400
    assert "minOrder" in response.json["error"]


def test_promo_unknown(client):
    """4. Code inconnu → 404"""
    payload = {
        "promoCode": "FauxCode123",
        "subtotal": 100,
        "current_date": "2026-04-09",
    }
    response = client.post("/promo/validate", json=payload)
    assert response.status_code == 404
    assert response.json["error"] == "Code inconnu"


def test_promo_missing_code_in_body(client):
    """5. Sans code dans le body → 400"""
    payload = {
        "subtotal": 100  # Manque promoCode
    }
    response = client.post("/promo/validate", json=payload)
    assert response.status_code == 400
    assert "Missing" in response.json["error"]
