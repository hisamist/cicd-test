from flask import Flask, jsonify, request
from src.pricing.price import calculate_order_total, apply_promo_code
import src.database as db

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({"message": "Hello World"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/orders/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    try:
        result = calculate_order_total(
            items=data.get("items", []),
            distance=data.get("distance", 0),
            weight=data.get("weight", 0),
            promo_code=data.get("promoCode", ""),
            hour=data.get("hour", ""),
            dayOfWeek=data.get("dayOfWeek", ""),
            current_date=data.get("currentDate", "2026-04-09"),
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    try:
        # 1. Calcul via le moteur
        result = calculate_order_total(
            items=data.get("items"),
            distance=data.get("distance"),
            weight=data.get("weight"),
            promo_code=data.get("promoCode", ""),
            hour=data.get("hour"),
            dayOfWeek=data.get("dayOfWeek"),
            current_date=data.get("currentDate", "2026-04-09"),
        )

        # 2. Utilisation de db.next_id pour éviter les copies locales
        order_id = db.next_id
        new_order = {
            "id": order_id,
            "items": data.get("items"),
            "total": result["total"],
            "subtotal": result["subtotal"],
            "deliveryFee": result["deliveryFee"],
            "discount": result["discount"],
        }

        # 3. Sauvegarde dans le dictionnaire partagé
        db.orders_db[order_id] = new_order

        # 4. Incrémentation de la variable originale dans le module
        db.next_id += 1

        return jsonify(new_order), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    try:
        # Recherche dans le dictionnaire partagé
        order = db.orders_db.get(order_id)

        if order:
            return jsonify(order), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/promo/validate", methods=["POST"])
def validate_promo():
    data = request.get_json() or {}
    promo_code = data.get("promoCode")
    subtotal = data.get("subtotal")
    current_date = data.get("current_date")

    if promo_code is None or subtotal is None:
        return jsonify({"error": "Missing promoCode or subtotal"}), 400

    try:
        discount_amount = apply_promo_code(
            subtotal=subtotal,
            promo_code=promo_code,
            promo_codes=db.PROMO_CODES,
            current_date=current_date,
        )

        # Chercher les infos du code pour le type et la valeur
        promo_info = next(p for p in db.PROMO_CODES if p["code"] == promo_code)

        # Test 1 : Code valide
        return jsonify(
            {
                "status": "valid",
                "discount_amount": discount_amount,
                "type": promo_info["type"],
                "value": promo_info["value"],
            }
        ), 200

    except ValueError as e:
        error_msg = str(e)
        if error_msg == "invalid code":
            return jsonify({"error": "Code inconnu"}), 404
        return jsonify({"error": error_msg}), 400
