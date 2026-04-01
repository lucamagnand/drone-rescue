# =============================================================================
# Corrigé — Module P02 : logique.py — fonctions factory
# Fichier cible dans jeu/ : jeu/logique.py
# =============================================================================
import random

# NIVEAU 1 — Fonctions factory minimales
# -----------------------------------------------------------------------------

def creer_drone(drone_id, col, lig, batterie_max=20):
    """Crée et retourne un nouveau dict représentant un drone.

    Chaque appel produit un objet indépendant.
    """
    return {
        "id":           drone_id,
        "col":          col,
        "lig":          lig,
        "batterie":     batterie_max,
        "batterie_max": batterie_max,
        "survivant":    None,   # id du survivant transporté, sinon None
        "bloque":       0,      # nombre de tours de blocage restants
        "hors_service": False,
    }


def creer_survivant(surv_id, col, lig):
    """Crée et retourne un nouveau dict représentant un survivant."""
    return {
        "id":   surv_id,
        "col":  col,
        "lig":  lig,
        "etat": "en_attente",  # 'en_attente' | 'embarque' | 'sauve'
    }


def creer_tempete(temp_id, col, lig, dx=1, dy=0):
    """Crée et retourne un nouveau dict représentant une tempête."""
    return {
        "id":  temp_id,
        "col": col,
        "lig": lig,
        "dx":  dx,   # direction x automatique
        "dy":  dy,   # direction y automatique
    }


# NIVEAU 2 — initialiser_partie() avec placement sans chevauchement
# -----------------------------------------------------------------------------

def initialiser_partie(config):
    """Crée l'état global initial prêt à jouer.

    Place toutes les entités sur la grille sans chevauchement.

    Args:
        config (dict): configuration issue de config.json.
    Returns:
        dict: état global initialisé.
    """
    taille       = config.get("GRILLE_TAILLE", 12)
    batterie_max = config.get("BATTERIE_MAX", 20)
    nb_drones    = config.get("NB_DRONES", 2)
    nb_surv      = config.get("NB_SURVIVANTS", 3)
    nb_tempetes  = config.get("NB_TEMPETES", 1)
    hop_col      = config.get("HOPITAL_COL", 0)
    hop_lig      = config.get("HOPITAL_LIG", 0)

    grille   = [[" . "] * taille for _ in range(taille)]
    occupees = set()

    # Placer l'hôpital
    grille[hop_lig][hop_col] = " H "
    occupees.add((hop_col, hop_lig))

    def pos_libre():
        """Génère une position (col, lig) aléatoire non occupée."""
        while True:
            col = random.randint(0, taille - 1)
            lig = random.randint(0, taille - 1)
            if (col, lig) not in occupees:
                occupees.add((col, lig))
                return col, lig

    # Créer les drones
    drones = {}
    for i in range(1, nb_drones + 1):
        d_id = f"D{i}"
        col, lig = pos_libre()
        drones[d_id] = creer_drone(d_id, col, lig, batterie_max)
        grille[lig][col] = " D "

    # Créer les survivants
    survivants = {}
    for i in range(1, nb_surv + 1):
        s_id = f"S{i}"
        col, lig = pos_libre()
        survivants[s_id] = creer_survivant(s_id, col, lig)
        grille[lig][col] = " S "

    # Créer les tempêtes
    tempetes = {}
    for i in range(1, nb_tempetes + 1):
        t_id = f"T{i}"
        col, lig = pos_libre()
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        tempetes[t_id] = creer_tempete(t_id, col, lig, dx, dy)
        grille[lig][col] = " T "

    return {
        "tour":         0,
        "score":        0,
        "partie_finie": False,
        "victoire":     False,
        "grille":       grille,
        "hopital":      (hop_col, hop_lig),
        "batiments":    [],
        "drones":       drones,
        "tempetes":     tempetes,
        "survivants":   survivants,
        "zones_x":      set(),
        "historique":   [],
    }


# NIVEAU 3 — Tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Test factory
    d1 = creer_drone("D1", 0, 0, 20)
    d2 = creer_drone("D2", 5, 5, 20)
    assert d1 is not d2, "Les drones doivent être des objets distincts"
    assert d1["batterie"] == 20
    assert d1["hors_service"] == False
    print("✅ creer_drone OK")

    s1 = creer_survivant("S1", 3, 7)
    assert s1["etat"] == "en_attente"
    print("✅ creer_survivant OK")

    t1 = creer_tempete("T1", 6, 6)
    assert t1["dx"] == 1
    print("✅ creer_tempete OK")

    config = {
        "GRILLE_TAILLE": 12, "BATTERIE_MAX": 20,
        "NB_DRONES": 2, "NB_SURVIVANTS": 3, "NB_TEMPETES": 1,
        "HOPITAL_COL": 0, "HOPITAL_LIG": 0,
    }
    etat = initialiser_partie(config)
    assert len(etat["drones"]) == 2
    assert len(etat["survivants"]) == 3
    assert etat["grille"][0][0] == " H "
    print("✅ initialiser_partie OK")
    print(f"   Drones : {list(etat['drones'].keys())}")
    print(f"   Survivants : {list(etat['survivants'].keys())}")
