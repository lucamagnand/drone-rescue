# =============================================================================
# Corrigé — Module P06 : Cas limites (collision, hors service, zones X, météo)
# Fichier cible dans jeu/ : jeu/logique.py — extensions executer_mouvement(),
#                           deplacer_tempetes(), propager_zones_x(),
#                           verifier_fin_partie()
# =============================================================================

import random

GRILLE_TAILLE = 12


# NIVEAU 1 — Solution minimale (zone X + hors_service + collision)
# -----------------------------------------------------------------------------

def appliquer_surcoût_zone_x(etat, id_drone, col_cible, lig_cible):
    """Applique le surcoût +2 si la case cible est une zone X."""
    drone = etat["drones"][id_drone]
    if (col_cible, lig_cible) in etat["zones_x"]:
        drone["batterie"] -= 2
    if drone["batterie"] <= 0:
        drone["batterie"] = 0
        drone["hors_service"] = True
        etat["grille"][lig_cible][col_cible] = "."
        return f"{id_drone} HORS SERVICE — batterie épuisée en zone X"
    return ""


def verifier_collision(etat, id_drone):
    """Vérifie si le drone est en collision avec une tempête."""
    drone = etat["drones"][id_drone]
    for tid, tempete in etat["tempetes"].items():
        if tempete["col"] == drone["col"] and tempete["lig"] == drone["lig"]:
            drone["bloque"] = 2
            return f"{id_drone} BLOQUÉ par {tid} — 2 tours"
    return ""


# NIVEAU 2 — Enrichissement (phase météo + propagation zones X)
# -----------------------------------------------------------------------------

def deplacer_tempetes(etat):
    """
    Phase météo automatique : chaque tempête a 50% de chance
    de se déplacer d'une case selon son vecteur (dx, dy).
    Rebondit sur les bords de la grille.
    """
    for tid, t in etat["tempetes"].items():
        if random.random() < 0.5:
            etat["grille"][t["lig"]][t["col"]] = "."
            t["col"] = max(0, min(GRILLE_TAILLE - 1, t["col"] + t["dx"]))
            t["lig"] = max(0, min(GRILLE_TAILLE - 1, t["lig"] + t["dy"]))
            etat["grille"][t["lig"]][t["col"]] = tid


def propager_zones_x(etat, probabilite=0.3):
    """
    Propage les zones dangereuses : chaque zone X peut contaminer
    ses voisins directs (4 directions) avec la probabilité donnée.
    Utilise un set temporaire pour éviter de modifier l'ensemble
    pendant l'itération.
    """
    nouvelles = set()
    for (col, lig) in list(etat["zones_x"]):
        for dcol, dlig in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nc, nl = col + dcol, lig + dlig
            if 0 <= nc < GRILLE_TAILLE and 0 <= nl < GRILLE_TAILLE:
                if random.random() < probabilite:
                    nouvelles.add((nc, nl))
    etat["zones_x"] |= nouvelles
    for (col, lig) in nouvelles:
        if etat["grille"][lig][col] == ".":
            etat["grille"][lig][col] = "X"


# NIVEAU 3 — Version complète intégrable dans jeu/logique.py
# -----------------------------------------------------------------------------

def verifier_fin_partie(etat, TOURS_MAX=50):
    """
    Vérifie les 3 conditions de fin de partie.
    Modifie etat['partie_finie'] et etat['victoire'] si une condition est remplie.
    Retourne un str de message ou '' si la partie continue.
    """
    survivants = etat["survivants"]
    drones = etat["drones"]

    # Victoire : tous les survivants sauvés
    if all(s["etat"] == "sauve" for s in survivants.values()):
        etat["partie_finie"] = True
        etat["victoire"] = True
        return "Victoire ! Tous les survivants sont en sécurité."

    # Défaite : tous les drones hors service
    if all(d["hors_service"] for d in drones.values()):
        etat["partie_finie"] = True
        etat["victoire"] = False
        return "Défaite — tous les drones sont hors service."

    # Défaite : nombre maximum de tours atteint
    if etat["tour"] >= TOURS_MAX:
        etat["partie_finie"] = True
        etat["victoire"] = False
        return f"Défaite — {TOURS_MAX} tours atteints sans sauver tous les survivants."

    return ""


def fin_de_tour(etat, TOURS_MAX=50):
    """
    Orchestre la fin d'un tour complet :
    1. Décrémenter les compteurs de blocage des drones
    2. Phase météo (déplacement aléatoire des tempêtes)
    3. Propagation des zones X (tous les 5 tours)
    4. Incrémenter le tour
    5. Vérifier fin de partie
    Retourne un str de log.
    """
    logs = []

    # 1. Décrémenter blocage
    for drone in etat["drones"].values():
        if drone["bloque"] > 0:
            drone["bloque"] -= 1

    # 2. Phase météo
    deplacer_tempetes(etat)
    logs.append("Phase météo exécutée.")

    # 3. Propagation zones X tous les 5 tours
    if etat["tour"] % 5 == 0 and etat["zones_x"]:
        propager_zones_x(etat)
        logs.append("Zones X propagées.")

    # 4. Incrémenter le tour
    etat["tour"] += 1

    # 5. Vérifier fin de partie
    msg_fin = verifier_fin_partie(etat, TOURS_MAX)
    if msg_fin:
        logs.append(msg_fin)

    return " | ".join(logs)


# --- Tests rapides ---
if __name__ == "__main__":
    random.seed(42)
    grille = [["." for _ in range(12)] for _ in range(12)]
    etat = {
        "tour": 1, "score": 0, "partie_finie": False, "victoire": False,
        "grille": grille, "hopital": (0, 0), "batiments": [],
        "drones": {
            "D1": {"id": "D1", "col": 3, "lig": 3,
                   "batterie": 3, "batterie_max": 20,
                   "survivant": None, "bloque": 0, "hors_service": False}
        },
        "tempetes": {
            "T1": {"id": "T1", "col": 5, "lig": 5, "dx": 1, "dy": 0}
        },
        "survivants": {
            "S1": {"id": "S1", "col": 4, "lig": 3, "etat": "en_attente"}
        },
        "zones_x": {(4, 3)},
        "historique": []
    }
    etat["grille"][0][0] = "H"
    etat["grille"][3][3] = "D1"
    etat["grille"][3][4] = "X"
    etat["grille"][5][5] = "T1"

    # Test zone X : D1 entre dans une zone X avec batterie=3
    # Après déplacement nominal : batterie = 3-1 = 2, zone X : 2-2 = 0 → hors_service
    etat["drones"]["D1"]["batterie"] -= 1  # simule coût déplacement
    log = appliquer_surcoût_zone_x(etat, "D1", 4, 3)
    print(log)
    assert etat["drones"]["D1"]["hors_service"]
    print("Test zone X OK")

    # Test fin de partie — victoire
    etat["survivants"]["S1"]["etat"] = "sauve"
    msg = verifier_fin_partie(etat)
    print(msg)
    assert etat["victoire"]
    print("Test victoire OK")
