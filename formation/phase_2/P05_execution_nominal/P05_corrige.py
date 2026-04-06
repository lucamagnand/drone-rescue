# =============================================================================
# Corrigé — Module P05 : Exécution nominale d'un mouvement
# Fichier cible dans jeu/ : jeu/logique.py — fonction executer_mouvement()
# =============================================================================

# NIVEAU 1 — Solution minimale (déplacement seul, batterie, grille)
# -----------------------------------------------------------------------------

def executer_mouvement_v1(etat, id_drone, col_cible, lig_cible):
    """Déplace un drone et met à jour la grille et la batterie."""
    drone = etat["drones"][id_drone]
    col_avant, lig_avant = drone["col"], drone["lig"]

    # Effacer l'ancienne position
    etat["grille"][lig_avant][col_avant] = "."

    # Déplacer
    drone["col"], drone["lig"] = col_cible, lig_cible

    # Consommer la batterie
    drone["batterie"] -= 1

    # Marquer la nouvelle position
    etat["grille"][lig_cible][col_cible] = id_drone

    return f"{id_drone} déplacé en ({col_cible},{lig_cible}), batterie={drone['batterie']}"


# NIVEAU 2 — Enrichissement (prise de survivant, coût transport)
# -----------------------------------------------------------------------------

def executer_mouvement_v2(etat, id_drone, col_cible, lig_cible):
    """Déplacement + prise de survivant + coût de transport."""
    drone = etat["drones"][id_drone]
    col_avant, lig_avant = drone["col"], drone["lig"]

    etat["grille"][lig_avant][col_avant] = "."
    drone["col"], drone["lig"] = col_cible, lig_cible

    # Coût : +1 si transport d'un survivant
    cout = 1
    if drone["survivant"] is not None:
        cout += 1
    drone["batterie"] -= cout

    # Prise de survivant en attente sur la case cible
    for sid, surv in etat["survivants"].items():
        if (surv["col"] == col_cible and surv["lig"] == lig_cible
                and surv["etat"] == "en_attente"):
            drone["survivant"] = sid
            surv["etat"] = "embarque"
            break

    etat["grille"][lig_cible][col_cible] = id_drone
    return f"{id_drone} en ({col_cible},{lig_cible}), batterie={drone['batterie']}"


# NIVEAU 3 — Version complète intégrable dans jeu/logique.py
# -----------------------------------------------------------------------------

def executer_mouvement(etat, id_drone, col_cible, lig_cible):
    """
    Déplace le drone id_drone vers (col_cible, lig_cible).

    Gère :
    - mise à jour double (dictionnaire drone + grille)
    - coût batterie (1 seul, +1 si transport survivant)
    - prise de survivant en_attente
    - livraison à l'hôpital (score +1, recharge +3)
    - recharge si stationnaire

    Précondition : valider_mouvement() a retourné (True, ...).
    Retourne un str de log décrivant l'action.
    """
    drone = etat["drones"][id_drone]
    col_avant, lig_avant = drone["col"], drone["lig"]

    # 1. Effacer l'ancienne position sur la grille
    etat["grille"][lig_avant][col_avant] = "."

    # 2. Déplacer le drone
    drone["col"], drone["lig"] = col_cible, lig_cible

    # 3. Calcul du coût batterie
    cout = 1
    if drone["survivant"] is not None:
        cout += 1  # +1 si transport d'un survivant
    drone["batterie"] -= cout

    # 4. Prise de survivant en_attente sur la case cible
    for sid, surv in etat["survivants"].items():
        if (surv["col"] == col_cible and surv["lig"] == lig_cible
                and surv["etat"] == "en_attente"):
            drone["survivant"] = sid
            surv["etat"] = "embarque"
            break

    # 5. Livraison à l'hôpital
    hop_col, hop_lig = etat["hopital"]
    if (col_cible == hop_col and lig_cible == hop_lig
            and drone["survivant"] is not None):
        sid = drone["survivant"]
        etat["survivants"][sid]["etat"] = "sauve"
        drone["survivant"] = None
        etat["score"] += 1
        drone["batterie"] = min(drone["batterie"] + 3, drone["batterie_max"])
        log_livraison = f" — {sid} sauvé ! Score={etat['score']}"
    else:
        log_livraison = ""

    # 6. Recharge si stationnaire
    if col_cible == col_avant and lig_cible == lig_avant:
        drone["batterie"] = min(drone["batterie"] + 3, drone["batterie_max"])

    # 7. Marquer la nouvelle position sur la grille
    etat["grille"][lig_cible][col_cible] = id_drone

    return (
        f"{id_drone} → ({col_cible},{lig_cible})"
        f", batterie={drone['batterie']}"
        f"{log_livraison}"
    )


# --- Tests rapides ---
if __name__ == "__main__":
    grille = [["." for _ in range(12)] for _ in range(12)]
    etat = {
        "tour": 1, "score": 0, "partie_finie": False, "victoire": False,
        "grille": grille,
        "hopital": (0, 0),
        "batiments": [],
        "drones": {
            "D1": {"id": "D1", "col": 3, "lig": 3,
                   "batterie": 15, "batterie_max": 20,
                   "survivant": None, "bloque": 0, "hors_service": False}
        },
        "tempetes": {},
        "survivants": {
            "S1": {"id": "S1", "col": 4, "lig": 3, "etat": "en_attente"}
        },
        "zones_x": set(),
        "historique": []
    }
    etat["grille"][0][0] = "H"
    etat["grille"][3][3] = "D1"
    etat["grille"][3][4] = "S1"

    # Test 1 : déplacement vers survivant
    log = executer_mouvement(etat, "D1", 4, 3)
    print(log)
    assert etat["drones"]["D1"]["survivant"] == "S1"
    assert etat["survivants"]["S1"]["etat"] == "embarque"
    print("Test 1 OK")

    # Test 2 : livraison à l'hôpital
    etat["drones"]["D1"]["col"] = 1
    etat["drones"]["D1"]["lig"] = 0
    etat["grille"][3][4] = "."
    etat["grille"][0][1] = "D1"
    log = executer_mouvement(etat, "D1", 0, 0)
    print(log)
    assert etat["score"] == 1
    assert etat["drones"]["D1"]["survivant"] is None
    print("Test 2 OK")
