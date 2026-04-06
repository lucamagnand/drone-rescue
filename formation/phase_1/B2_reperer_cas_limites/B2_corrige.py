# =============================================================================
# B2_corrige.py — Repérer les cas limites avant de coder
# Trois niveaux de maîtrise
# =============================================================================

TAILLE = 12
LETTRES = "ABCDEFGHIJKL"

etat_test = {
    'grille': [['.' for _ in range(TAILLE)] for _ in range(TAILLE)],
    'drones': {
        'D1': {'col': 3, 'lig': 3, 'batterie': 5, 'en_service': True,  'charge': None},
        'D2': {'col': 0, 'lig': 0, 'batterie': 0, 'en_service': True,  'charge': 'S1'},
        'D3': {'col': 2, 'lig': 2, 'batterie': 3, 'en_service': False, 'charge': None},
    }
}
etat_test['grille'][4][4] = 'B'   # bâtiment en E5 (col=4, lig=4)


# -----------------------------------------------------------------------------
# NIVEAU 1 — est_case_valide
# -----------------------------------------------------------------------------

def est_case_valide(col, lig):
    """Renvoie True si (col, lig) est dans la grille 12x12."""
    return 0 <= col <= 11 and 0 <= lig <= 11


assert est_case_valide(0,  0)  == True
assert est_case_valide(11, 11) == True
assert est_case_valide(12, 0)  == False
assert est_case_valide(0,  12) == False
assert est_case_valide(-1, 0)  == False
assert est_case_valide(0, -1)  == False


# -----------------------------------------------------------------------------
# NIVEAU 2 — peut_se_deplacer (4 conditions)
# -----------------------------------------------------------------------------

def peut_se_deplacer(etat, id_drone, col_cible, lig_cible):
    """Vérifie si le drone peut se déplacer vers (col_cible, lig_cible)."""
    drone = etat['drones'][id_drone]
    # 1 : case dans la grille
    if not est_case_valide(col_cible, lig_cible):
        return False
    # 2 : case pas un bâtiment
    if etat['grille'][lig_cible][col_cible] == 'B':
        return False
    # 3 : batterie > 0
    if drone['batterie'] <= 0:
        return False
    # 4 : drone en service
    if not drone['en_service']:
        return False
    return True


# Cas nominal
assert peut_se_deplacer(etat_test, 'D1', 5, 5)  == True
# Cas limite : hors grille
assert peut_se_deplacer(etat_test, 'D1', 12, 0) == False
assert peut_se_deplacer(etat_test, 'D1', -1, 0) == False
# Cas limite : bâtiment
assert peut_se_deplacer(etat_test, 'D1', 4, 4)  == False
# Cas limite : batterie = 0
assert peut_se_deplacer(etat_test, 'D2', 1, 1)  == False
# Cas limite : drone hors service
assert peut_se_deplacer(etat_test, 'D3', 1, 1)  == False


# -----------------------------------------------------------------------------
# NIVEAU 3 — Tableau complet des cas limites de valider_mouvement
# (préfiguration de P04)
# -----------------------------------------------------------------------------

def valider_mouvement_complet(etat, id_drone, col_cible, lig_cible):
    """
    Validation complète préfigurant P04 :
    - case dans la grille
    - case pas un bâtiment
    - batterie suffisante (>0 ; >1 si portage survivant)
    - drone en service
    """
    drone = etat['drones'][id_drone]
    if not est_case_valide(col_cible, lig_cible):
        return False, "Hors grille"
    if etat['grille'][lig_cible][col_cible] == 'B':
        return False, "Bâtiment"
    cout = 2 if drone['charge'] is not None else 1
    if drone['batterie'] < cout:
        return False, "Batterie insuffisante"
    if not drone['en_service']:
        return False, "Drone hors service"
    return True, "OK"


assert valider_mouvement_complet(etat_test, 'D1', 5, 5)  == (True, "OK")
assert valider_mouvement_complet(etat_test, 'D1', 12, 0) == (False, "Hors grille")
assert valider_mouvement_complet(etat_test, 'D1', 4, 4)  == (False, "B\u00e2timent")
assert valider_mouvement_complet(etat_test, 'D2', 1, 1)  == (False, "Batterie insuffisante")
assert valider_mouvement_complet(etat_test, 'D3', 1, 1)  == (False, "Drone hors service")

print("Tous les assert B2 passent ✓")
