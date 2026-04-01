# =============================================================================
# Corrigé — Module B0 : Tracer un programme à la main
# Fichier cible dans jeu/ : jeu/logique.py — executer_mouvement()
# =============================================================================
#
# NIVEAU 1 — Solution minimale : executer_mouvement() avec print de debug
# -----------------------------------------------------------------------------

def executer_mouvement_v1(etat, drone_id, col_dest, lig_dest):
    """Déplace le drone et met à jour toutes les structures concernées.

    Version minimale avec print de debug pour visualiser le traçage.

    Args:
        etat (dict): état global du jeu.
        drone_id (str): identifiant du drone à déplacer (ex: 'D1').
        col_dest (int): colonne de destination (0-11).
        lig_dest (int): ligne de destination (0-11).

    Returns:
        str: log de l'action exécutée.
    """
    drone = etat["drones"][drone_id]

    # Sauvegarder les coordonnées avant le mouvement
    col_avant = drone["col"]
    lig_avant = drone["lig"]
    print(f"[DEBUG] {drone_id} avant : ({col_avant},{lig_avant}), batterie={drone['batterie']}")

    # Mettre à jour les coordonnées du drone
    drone["col"] = col_dest
    drone["lig"] = lig_dest
    print(f"[DEBUG] coords : ({col_avant},{lig_avant}) → ({col_dest},{lig_dest})")

    # Mettre à jour la grille
    etat["grille"][lig_avant][col_avant] = " . "  # effacer l'ancienne case
    etat["grille"][lig_dest][col_dest] = " D "    # marquer la nouvelle case
    print(f"[DEBUG] grille mise à jour")

    # Calculer le coût
    cout = 1
    if (col_dest, lig_dest) in etat["zones_x"]:
        cout += 2
        print(f"[DEBUG] zone X sur ({col_dest},{lig_dest}) → coût={cout}")

    # Consommer la batterie
    drone["batterie"] -= cout
    print(f"[DEBUG] batterie après : {drone['batterie']}")

    return f"{drone_id}:({col_avant},{lig_avant})->({col_dest},{lig_dest}), batterie={drone['batterie']}"


# NIVEAU 2 — Enrichissement : gestion de la batterie à zéro (hors service)
# -----------------------------------------------------------------------------

def executer_mouvement_v2(etat, drone_id, col_dest, lig_dest):
    """Déplace le drone avec gestion du cas batterie à zéro.

    Si la batterie tombe à 0 ou moins après le déplacement,
    le drone est marqué hors_service.
    """
    drone = etat["drones"][drone_id]
    col_avant = drone["col"]
    lig_avant = drone["lig"]

    drone["col"] = col_dest
    drone["lig"] = lig_dest

    etat["grille"][lig_avant][col_avant] = " . "
    etat["grille"][lig_dest][col_dest] = " D "

    cout = 1
    if (col_dest, lig_dest) in etat["zones_x"]:
        cout += 2

    drone["batterie"] -= cout

    # Cas limite : batterie épuisée en vol → hors service définitivement
    if drone["batterie"] <= 0:
        drone["batterie"] = 0
        drone["hors_service"] = True
        etat["grille"][lig_dest][col_dest] = " . "  # le drone disparaît
        return f"{drone_id} hors service sur ({col_dest},{lig_dest}) — batterie épuisée"

    return f"{drone_id}:({col_avant},{lig_avant})->({col_dest},{lig_dest}), batterie={drone['batterie']}"


# NIVEAU 3 — Version complète intégrable dans jeu/ (proche du code réel)
# -----------------------------------------------------------------------------

def executer_mouvement_v3(etat, drone_id, col_dest, lig_dest):
    """Exécute le déplacement d'un drone et met à jour l'état complet.

    Gère : mise à jour coordonnées, grille, batterie, transport de survivant,
    collision avec tempête, zones X, hors service.

    Args:
        etat (dict): état global du jeu.
        drone_id (str): identifiant du drone ('D1', 'D2', ...).
        col_dest (int): colonne de destination (0-11).
        lig_dest (int): ligne de destination (0-11).

    Returns:
        str: message de log décrivant l'action effectuée.
    """
    drone = etat["drones"][drone_id]
    col_avant = drone["col"]
    lig_avant = drone["lig"]

    # 1. Mettre à jour les coordonnées
    drone["col"] = col_dest
    drone["lig"] = lig_dest

    # 2. Mettre à jour la grille
    symbole_drone = " D "
    etat["grille"][lig_avant][col_avant] = " . "
    etat["grille"][lig_dest][col_dest] = symbole_drone

    # 3. Calculer le coût
    cout = 1
    if drone.get("survivant"):  # transport d'un survivant : +1
        cout += 1
    if (col_dest, lig_dest) in etat["zones_x"]:  # zone dangereuse : +2
        cout += 2

    drone["batterie"] -= cout

    # 4. Cas limite : batterie épuisée
    if drone["batterie"] <= 0:
        drone["batterie"] = 0
        drone["hors_service"] = True
        etat["grille"][lig_dest][col_dest] = " . "
        return f"{drone_id} hors service — batterie épuisée sur ({col_dest},{lig_dest})"

    # 5. Recharge à l'hôpital
    col_h, lig_h = etat["hopital"]
    if col_dest == col_h and lig_dest == lig_h:
        gain = min(3, drone["batterie_max"] - drone["batterie"])
        drone["batterie"] += gain

        # Livraison du survivant à l'hôpital
        if drone.get("survivant"):
            surv_id = drone["survivant"]
            etat["survivants"][surv_id]["etat"] = "sauve"
            etat["score"] += 1
            drone["survivant"] = None
            return (
                f"{drone_id} livre {surv_id} à l'hôpital, "
                f"batterie={drone['batterie']}, score={etat['score']}"
            )

    return (
        f"{drone_id}:({col_avant},{lig_avant})->({col_dest},{lig_dest}), "
        f"batterie={drone['batterie']}"
    )


# --- Tests ---

if __name__ == "__main__":
    grille = [[" . "] * 4 for _ in range(4)]
    grille[2][1] = " D "
    drone = {
        "id": "D1", "col": 1, "lig": 2,
        "batterie": 10, "batterie_max": 20,
        "survivant": None, "bloque": 0, "hors_service": False
    }
    etat = {
        "drones": {"D1": drone},
        "grille": grille,
        "zones_x": set(),
        "hopital": (0, 0),
        "survivants": {},
        "score": 0,
    }

    # Test déplacement simple
    print("=== Test déplacement simple ===")
    log = executer_mouvement_v1(etat, "D1", 2, 2)
    print("Log :", log)
    assert drone["col"] == 2
    assert drone["lig"] == 2
    assert drone["batterie"] == 9
    assert grille[2][1] == " . "
    assert grille[2][2] == " D "
    print("✅ Déplacement simple OK")
