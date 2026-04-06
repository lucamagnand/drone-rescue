# =============================================================================
# Corrigé — Module A1 : Identifier les entités et leurs attributs
# Fichier cible dans jeu/ : jeu/logique.py (fonctions factory)
# =============================================================================

# NIVEAU 1 — Solution minimale
# -----------------------------------------------------------------------------

def creer_drone(identifiant, col, lig, batterie_max):
    """Retourne un dictionnaire représentant un nouveau drone.

    Args:
        identifiant (str): ex. 'D1'
        col (int): colonne initiale (0-basé, 0 = A)
        lig (int): ligne initiale (0-basé, 0 = ligne 1)
        batterie_max (int): capacité maximale de la batterie

    Returns:
        dict: drone avec tous ses attributs initialisés
    """
    return {
        "id": identifiant,
        "col": col,
        "lig": lig,
        "batterie": batterie_max,
        "batterie_max": batterie_max,
        "survivant": None,
        "bloque": 0,
        "hors_service": False,
    }


def creer_survivant(identifiant, col, lig):
    """Retourne un dictionnaire représentant un nouveau survivant.

    Args:
        identifiant (str): ex. 'S1'
        col (int): colonne initiale
        lig (int): ligne initiale

    Returns:
        dict: survivant avec tous ses attributs initialisés
    """
    return {
        "id": identifiant,
        "col": col,
        "lig": lig,
        "etat": "en_attente",
    }


def creer_tempete(identifiant, col, lig, dx, dy):
    """Retourne un dictionnaire représentant une nouvelle tempête.

    Args:
        identifiant (str): ex. 'T1'
        col (int): colonne initiale
        lig (int): ligne initiale
        dx (int): direction colonne (-1, 0 ou +1)
        dy (int): direction ligne (-1, 0 ou +1)

    Returns:
        dict: tempête avec tous ses attributs initialisés
    """
    return {
        "id": identifiant,
        "col": col,
        "lig": lig,
        "dx": dx,
        "dy": dy,
    }


# NIVEAU 2 — Enrichissement (validation des paramètres)
# -----------------------------------------------------------------------------

ETATS_SURVIVANT = {"en_attente", "embarque", "sauve"}


def creer_drone_v2(identifiant, col, lig, batterie_max):
    """Crée un drone avec validation des paramètres."""
    if not isinstance(identifiant, str) or not identifiant.startswith("D"):
        raise ValueError(f"Identifiant drone invalide : '{identifiant}'")
    if not (0 <= col <= 11 and 0 <= lig <= 11):
        raise ValueError(f"Coordonnées hors grille : col={col}, lig={lig}")
    if batterie_max <= 0:
        raise ValueError(f"batterie_max doit \u00eatre positif : {batterie_max}")
    return {
        "id": identifiant,
        "col": col,
        "lig": lig,
        "batterie": batterie_max,
        "batterie_max": batterie_max,
        "survivant": None,
        "bloque": 0,
        "hors_service": False,
    }


def creer_survivant_v2(identifiant, col, lig):
    """Crée un survivant avec validation."""
    if not isinstance(identifiant, str) or not identifiant.startswith("S"):
        raise ValueError(f"Identifiant survivant invalide : '{identifiant}'")
    if not (0 <= col <= 11 and 0 <= lig <= 11):
        raise ValueError(f"Coordonnées hors grille : col={col}, lig={lig}")
    return {
        "id": identifiant,
        "col": col,
        "lig": lig,
        "etat": "en_attente",
    }


# NIVEAU 3 — Version complète intégrable dans jeu/logique.py
# -----------------------------------------------------------------------------
# Ces versions correspondent au code réel de jeu/logique.py.
# Elles intègrent la lecture des constantes depuis config.py.

def creer_drone_v3(identifiant, col, lig, batterie_max):
    """Version de production de creer_drone().

    Identique à creer_drone() niveau 1 dans la structure,
    mais utilisée avec les constantes issues de config.py :

        from config import BATTERIE_MAX
        drone = creer_drone_v3('D1', col=0, lig=0, batterie_max=BATTERIE_MAX)
    """
    return {
        "id": identifiant,
        "col": col,
        "lig": lig,
        "batterie": batterie_max,
        "batterie_max": batterie_max,
        "survivant": None,
        "bloque": 0,
        "hors_service": False,
    }


# --- Tests de validation ---
if __name__ == "__main__":
    d = creer_drone("D1", 0, 0, 10)
    assert d["id"] == "D1"
    assert d["batterie"] == d["batterie_max"] == 10
    assert d["survivant"] is None
    assert d["bloque"] == 0
    assert d["hors_service"] is False
    print("✅ creer_drone : OK")

    s = creer_survivant("S1", 5, 5)
    assert s["etat"] == "en_attente"
    print("✅ creer_survivant : OK")

    t = creer_tempete("T1", 10, 10, -1, 0)
    assert t["dx"] == -1
    assert t["dy"] == 0
    print("✅ creer_tempete : OK")
