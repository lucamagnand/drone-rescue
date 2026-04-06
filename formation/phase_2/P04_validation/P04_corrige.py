# =============================================================================
# Corrigé — Module P04 : Validation de mouvement
# Fichier cible dans jeu/ : jeu/logique.py
#   Fonction principale : valider_mouvement(etat, drone_id, col_cible, lig_cible)
# =============================================================================


# Constantes (en production, viennent de config.py)
GRILLE_TAILLE = 12


# NIVEAU 1 — Solution minimale (4 cas fondamentaux)
# -----------------------------------------------------------------------------
# Vérifie : existence du drone, hors grille, bâtiment, distance.

def valider_mouvement_n1(etat, drone_id, col_cible, lig_cible):
    """
    Validation minimale — 4 règles.
    Retourne (True, '') si valide, (False, message) sinon.
    """
    # 1. Le drone existe-t-il ?
    if drone_id not in etat["drones"]:
        return False, f"Drone {drone_id} inexistant"
    drone = etat["drones"][drone_id]

    # 2. Cible dans la grille ?
    if not (0 <= col_cible < GRILLE_TAILLE and 0 <= lig_cible < GRILLE_TAILLE):
        return False, "Position hors grille"

    # 3. Cible non bloquée ?
    if etat["grille"][lig_cible][col_cible] == 'B':
        return False, "Bâtiment infranchissable"

    # 4. Distance Chebyshev ≤ 1 ?
    distance = max(abs(col_cible - drone["col"]), abs(lig_cible - drone["lig"]))
    if distance > 1:
        return False, f"Distance {distance} > 1"

    return True, ""


# NIVEAU 2 — Enrichissement (batterie, hors_service, bloqué)
# -----------------------------------------------------------------------------

def valider_mouvement_n2(etat, drone_id, col_cible, lig_cible):
    """
    Validation enrichie — 6 règles (ajout batterie, hors_service, bloqué).
    """
    if drone_id not in etat["drones"]:
        return False, f"Drone {drone_id} inexistant"
    drone = etat["drones"][drone_id]

    if drone["hors_service"]:
        return False, f"{drone_id} est hors service"
    if drone["bloque"] > 0:
        return False, f"{drone_id} est bloqué ({drone['bloque']} tour(s))"

    distance = max(abs(col_cible - drone["col"]), abs(lig_cible - drone["lig"]))
    if distance > 1:
        return False, f"Distance {distance} > 1 case autorisée"

    if not (0 <= col_cible < GRILLE_TAILLE and 0 <= lig_cible < GRILLE_TAILLE):
        return False, "Position hors grille"

    if etat["grille"][lig_cible][col_cible] == 'B':
        return False, "Bâtiment infranchissable"

    if drone["batterie"] < 1:
        return False, "Batterie insuffisante"

    return True, ""


# NIVEAU 3 — Version complète intégrable dans jeu/
# -----------------------------------------------------------------------------
# Identique au code réel de jeu/logique.py.
# Gère le cas stationnaire (distance == 0 → autorisé, consommation 0).

def valider_mouvement(etat, drone_id, col_cible, lig_cible):
    """
    Vérifie si le mouvement du drone vers (col_cible, lig_cible) est légal.

    Règles vérifiées (dans l'ordre) :
    1. Drone existe dans etat['drones']
    2. Drone n'est pas hors_service
    3. Drone n'est pas bloqué
    4. Distance Chebyshev ≤ 1 (0 = rester sur place, autorisé)
    5. Cible dans la grille
    6. Cible n'est pas un bâtiment ('B')
    7. Batterie ≥ 1 si déplacement réel (distance > 0)

    Retourne :
        (True, '')           si le mouvement est légal
        (False, message)     sinon, avec la raison du refus

    NE MODIFIE JAMAIS etat.
    """
    if drone_id not in etat["drones"]:
        return False, f"Drone {drone_id} inexistant"
    drone = etat["drones"][drone_id]

    if drone["hors_service"]:
        return False, f"{drone_id} est hors service"
    if drone["bloque"] > 0:
        return False, f"{drone_id} est bloqué ({drone['bloque']} tour(s) restants)"

    distance = max(abs(col_cible - drone["col"]), abs(lig_cible - drone["lig"]))
    if distance > 1:
        return False, f"Distance Chebyshev = {distance} (max autorisé : 1)"

    if not (0 <= col_cible < GRILLE_TAILLE and 0 <= lig_cible < GRILLE_TAILLE):
        return False, f"Position ({col_cible}, {lig_cible}) hors grille"

    if etat["grille"][lig_cible][col_cible] == 'B':
        return False, "La case cible contient un bâtiment infranchissable"

    if distance > 0 and drone["batterie"] < 1:
        return False, f"{drone_id} : batterie à {drone['batterie']}, déplacement impossible"

    return True, ""


# -----------------------------------------------------------------------------
# Vérification rapide (tests unitaires avec assert)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Construction d'un état minimal pour les tests
    grille = [['.' for _ in range(GRILLE_TAILLE)] for _ in range(GRILLE_TAILLE)]
    grille[2][3] = 'B'  # bâtiment en (col=3, lig=2)

    etat = {
        "grille": grille,
        "drones": {
            "D1": {"id": "D1", "col": 3, "lig": 3, "batterie": 5,
                   "batterie_max": 20, "survivant": None,
                   "bloque": 0, "hors_service": False},
            "D2": {"id": "D2", "col": 5, "lig": 5, "batterie": 0,
                   "batterie_max": 20, "survivant": None,
                   "bloque": 0, "hors_service": False},
            "D3": {"id": "D3", "col": 7, "lig": 7, "batterie": 5,
                   "batterie_max": 20, "survivant": None,
                   "bloque": 2, "hors_service": False},
        }
    }

    # CAS VALIDES
    ok, msg = valider_mouvement(etat, "D1", 4, 3)   # déplacement d'1 case à droite
    assert ok, f"Attendu valide, obtenu : {msg}"

    ok, msg = valider_mouvement(etat, "D1", 3, 3)   # rester sur place
    assert ok, f"Attendu valide (stationnaire), obtenu : {msg}"

    ok, msg = valider_mouvement(etat, "D1", 4, 4)   # diagonale (distance Chebyshev = 1)
    assert ok, f"Attendu valide (diagonale), obtenu : {msg}"

    # CAS INVALIDES
    ok, msg = valider_mouvement(etat, "D1", 5, 3)   # distance = 2
    assert not ok and "Distance" in msg, f"Attendu invalide (distance), obtenu : ({ok}, {msg})"

    ok, msg = valider_mouvement(etat, "D1", 3, 2)   # bâtiment
    assert not ok and "bâtiment" in msg.lower(), f"Attendu invalide (bâtiment), obtenu : ({ok}, {msg})"

    ok, msg = valider_mouvement(etat, "D1", -1, 3)  # hors grille
    assert not ok and "hors" in msg.lower(), f"Attendu invalide (hors grille), obtenu : ({ok}, {msg})"

    ok, msg = valider_mouvement(etat, "D2", 6, 5)   # batterie = 0
    assert not ok and "batterie" in msg.lower(), f"Attendu invalide (batterie), obtenu : ({ok}, {msg})"

    ok, msg = valider_mouvement(etat, "D3", 8, 7)   # bloqué
    assert not ok and "bloqu" in msg.lower(), f"Attendu invalide (bloqué), obtenu : ({ok}, {msg})"

    ok, msg = valider_mouvement(etat, "D99", 3, 3)  # drone inexistant
    assert not ok and "inexistant" in msg.lower(), f"Attendu invalide (inexistant), obtenu : ({ok}, {msg})"

    print("✅ Tous les tests valider_mouvement() passent (6 cas invalides + 3 valides).")
