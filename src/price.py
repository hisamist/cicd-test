
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