# On garde les structures vides au départ ou avec tes datas
orders_db = {}
next_id = 1

# Liste des codes promos (Source de vérité unique)
PROMO_CODES = [
    {
        "code": "BIENVENUE20",
        "type": "percentage",
        "value": 20,
        "minOrder": 15.00,
        "expiresAt": "2026-12-31",
    },
    {
        "code": "PROMO5",
        "type": "fixed",
        "value": 5,
        "minOrder": 10.00,
        "expiresAt": "2026-12-31",
    },
    {
        "code": "PROMO10",
        "type": "fixed",
        "value": 10,
        "minOrder": 30.00,
        "expiresAt": "2026-12-31",
    },
    {
        "code": "PROMOMO",
        "type": "fixed",
        "value": 10,
        "minOrder": 0,
        "expiresAt": "2027-04-09",
    },
    {
        "code": "TODAY30",
        "type": "fixed",
        "value": 10,
        "minOrder": 0,
        "expiresAt": "2026-04-08",
    },
]


def reset_db():
    """Réinitialise la base de données en mémoire pour les tests."""
    global next_id
    # IMPORTANT: .clear() vide le dictionnaire existant sans changer sa référence
    orders_db.clear()
    # On réinitialise le compteur d'ID
    import src.database

    src.database.next_id = 1
