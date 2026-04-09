from datetime import datetime
from src.database import PROMO_CODES


# Calcule les frais de livraison selon la distance et le poids de la commande.
def calculate_delivery_fee(distance: int, weight: int):
    if distance <= 0 or weight <= 0:
        raise ValueError("negative")
    total_price = 2  # base price
    # Distance
    if distance <= 3:
        total_price += 0
    elif distance < 10:
        additional_distance = round(distance - 3)
        additional_price = 0.5 * additional_distance
        total_price += additional_price
    else:
        raise ValueError("refuse")

    if weight < 5:
        total_price += 0
    else:
        total_price += 1.5
    return total_price


def apply_promo_code(
    subtotal: int, promo_code: str, promo_codes: list[dict], current_date: str = None
):
    if subtotal < 0:
        raise ValueError("negative")
    if subtotal == 0:
        return 0
    if not promo_code:
        return subtotal

    if current_date is None:
        current_date = datetime.now().strftime("%Y-%m-%d")

    discount_value = 0
    for code in promo_codes:
        if promo_code.strip() == code["code"]:
            if subtotal < code["minOrder"]:
                raise ValueError("minOrder not met")
            if code["expiresAt"] < current_date:
                raise ValueError("code expired")
            if code["type"] == "percentage":
                discount_value = round(subtotal * code["value"] / 100)
            elif code["type"] == "fixed":
                discount_value = code["value"]

            final_price = subtotal - discount_value
            return float(max(0, final_price))

    raise ValueError("invalid code")


# Retourne le multiplicateur de prix selon l'heure et le jour.
# Le surge pricing augmente les frais de livraison en heures de pointe.
def calculate_surge(hour: str, dayOfWeek: str) -> float:
    if not hour or not dayOfWeek:
        raise ValueError("manque params")

    if hour < "10:00" or hour >= "22:00":
        return 0

    day = dayOfWeek.strip().lower()

    if day == "dimanche":
        return 1.2

    if day in ["lundi", "mardi", "mercredi", "jeudi"]:
        if "12:00" <= hour <= "13:30":
            return 1.3
        elif "19:00" <= hour <= "21:00":
            return 1.5
        else:
            return 1.0

    if day in ["vendredi", "samedi"]:
        if "19:00" <= hour <= "22:00":
            return 1.8


"""
La fonction principale qui assemble tout :

1. Calculer le sous-total des items (somme des price * quantity)
2. Appliquer le code promo (si fourni)
3. Calculer les frais de livraison
4. Appliquer le multiplicateur surge
5. Retourner : { subtotal, discount, deliveryFee, surge, total }
"""


def calculate_order_total(
    items: list[dict],
    distance: float,
    weight: float,
    promo_code: str,
    hour: str,
    dayOfWeek: str,
    current_date: str,
) -> float:
    if len(items) == 0:
        raise ValueError("empty items")
    if hour < "10:00" or hour >= "22:00":
        raise ValueError("Hors de service")

    subtotal = 0
    for i in items:
        if i["price"] <= 0:
            raise ValueError("Le prix est inadequate")
        subtotal += i["price"] * i["quantity"]
    discount = apply_promo_code(subtotal, promo_code, PROMO_CODES, current_date)
    surge_multiplier = calculate_surge(hour, dayOfWeek)
    final_delivery_fee = calculate_delivery_fee(distance, weight) * surge_multiplier
    total = discount + final_delivery_fee

    return {
        "subtotal": subtotal,
        "discount": discount,
        "deliveryFee": final_delivery_fee,
        "surge": surge_multiplier,
        "total": total,
    }
