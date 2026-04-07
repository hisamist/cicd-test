from datetime import datetime

# Calcule les frais de livraison selon la distance et le poids de la commande.
def calculate_delivery_fee(distance:int,weight:int):
    if distance <= 0 or weight <= 0:
        raise ValueError("negative")
    total_price = 2 # base price
    # Distance
    if distance <= 3 :
       total_price += 0
    elif distance < 10 : 
       additional_distance = round(distance - 3)
       additional_price = 0.5 * additional_distance
       total_price += additional_price
    else:
        raise ValueError("refuse")
           
    if weight < 5:
        total_price +=0
    else:
        total_price += 1.5
    return total_price

def apply_promo_code(subtotal:int,promo_code:str,promo_codes:list[dict]):
    if subtotal < 0 :
        raise ValueError("negative")
    if subtotal == 0:
        return 0
    if not promo_code: 
        return subtotal

    today_str = datetime.now().strftime("%Y-%m-%d")
    discount_value = 0
    for code in promo_codes:
        if promo_code.strip() == code["code"]:
            if subtotal < code["minOrder"]:
                    raise ValueError("minOrder not met")
            if code["expiresAt"] < today_str:
                    raise ValueError("code expired")
            if code["type"]=="percentage":
                discount_value = round(subtotal*code["value"]/100)
            elif code["type"] == "fixed":
                discount_value = code["value"]
            
            final_price = subtotal-discount_value
            return float(max(0, final_price))
   
    raise ValueError("invalid code")