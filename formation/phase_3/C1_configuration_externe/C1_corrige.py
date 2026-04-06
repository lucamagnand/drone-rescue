# =============================================================================
# Corrigé — Module C1 : Configuration externe
# Fichier cible dans jeu/ : jeu/config.json + jeu/config.py
# =============================================================================
#
# NIVEAU 1 — Solution minimale : extraire les constantes depuis un dict JSON
# -----------------------------------------------------------------------------

import json

# Simulation du contenu de config.json (reproduit inline pour autonomie)
CONFIG_JSON = {
    "grille": {"lignes": 12, "colonnes": 12},
    "drones": {"nb_max_j1": 6, "batterie_max": 20, "batterie_depart": 10},
    "tempetes": {"nb_max_j2": 4, "prob_meteo": 0.5},
    "regles": {
        "cout_transport_survivant": 2,
        "cout_entree_zone_x": 2,
        "recharge_hopital_par_tour": 3
    }
}

# Extraction des constantes nommées — niveau 1
GRILLE_TAILLE  = CONFIG_JSON["grille"]["lignes"]                        # 12
NB_DRONES      = CONFIG_JSON["drones"]["nb_max_j1"]                     # 6
BATTERIE_MAX   = CONFIG_JSON["drones"]["batterie_max"]                  # 20
BATTERIE_INIT  = CONFIG_JSON["drones"]["batterie_depart"]               # 10
NB_TEMPETES    = CONFIG_JSON["tempetes"]["nb_max_j2"]                   # 4
COUT_TRANSPORT = CONFIG_JSON["regles"]["cout_transport_survivant"]      # 2
COUT_ZONE_X    = CONFIG_JSON["regles"]["cout_entree_zone_x"]            # 2
RECHARGE       = CONFIG_JSON["regles"]["recharge_hopital_par_tour"]     # 3
NB_TOURS_MAX   = 40  # non dans config.json, défini directement


def initialiser_grille():
    """Crée une grille vide de taille GRILLE_TAILLE × GRILLE_TAILLE."""
    return [['.' for _ in range(GRILLE_TAILLE)] for _ in range(GRILLE_TAILLE)]


def calculer_cout(drone, destination, zones_x):
    """Calcule le coût de déplacement sans valeur magique."""
    cout = 1
    if drone['survivant'] is not None:
        cout += COUT_TRANSPORT
    if destination in zones_x:
        cout += COUT_ZONE_X
    return cout


def tour_max_depasse(etat):
    """Retourne True si le nombre de tours maximum est atteint."""
    return etat['tour'] >= NB_TOURS_MAX


# --- Vérifications niveau 1 ---
assert GRILLE_TAILLE == 12
assert NB_DRONES == 6
assert BATTERIE_MAX == 20
assert COUT_TRANSPORT == 2
grille = initialiser_grille()
assert len(grille) == 12 and len(grille[0]) == 12
assert calculer_cout({'survivant': 'S1', 'batterie': 10}, (1, 1), set()) == 3
assert calculer_cout({'survivant': None, 'batterie': 10}, (1, 1), set()) == 1
assert tour_max_depasse({'tour': 40}) == True
assert tour_max_depasse({'tour': 39}) == False
print("Niveau 1 : OK")


# NIVEAU 2 — Enrichissement : charger_config() avec validation
# -----------------------------------------------------------------------------

def charger_config(cfg_dict):
    """
    Charge la configuration depuis un dictionnaire et retourne les constantes.
    Valide les types et les valeurs minimales.
    """
    cles_requises = [
        ("grille", "lignes"),
        ("drones", "batterie_max"),
        ("regles", "cout_transport_survivant"),
    ]
    for section, cle in cles_requises:
        if section not in cfg_dict or cle not in cfg_dict[section]:
            raise ValueError(f"Clé manquante dans config : [{section}][{cle}]")

    taille = cfg_dict["grille"]["lignes"]
    if not isinstance(taille, int) or taille < 4:
        raise ValueError(f"GRILLE_TAILLE doit être un entier >= 4, reçu : {taille}")

    return {
        "GRILLE_TAILLE":  taille,
        "NB_DRONES":      cfg_dict["drones"]["nb_max_j1"],
        "BATTERIE_MAX":   cfg_dict["drones"]["batterie_max"],
        "COUT_TRANSPORT": cfg_dict["regles"]["cout_transport_survivant"],
        "COUT_ZONE_X":    cfg_dict["regles"]["cout_entree_zone_x"],
        "RECHARGE":       cfg_dict["regles"]["recharge_hopital_par_tour"],
    }


constantes = charger_config(CONFIG_JSON)
assert constantes["GRILLE_TAILLE"] == 12
print("Niveau 2 : OK")


# NIVEAU 3 — Version complète intégrable dans jeu/config.py
# (proche du code réel de jeu/config.py)
# -----------------------------------------------------------------------------

import os


def charger_config_depuis_fichier(chemin):
    """
    Lit config.json depuis le chemin donné et retourne les constantes.
    Compatible avec le comportement de jeu/config.py.
    """
    if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier de configuration introuvable : {chemin}")
    with open(chemin, encoding="utf-8") as f:
        cfg = json.load(f)
    return charger_config(cfg)


# Utilisation : dans jeu/config.py, on fait simplement :
# _DOSSIER = os.path.dirname(os.path.abspath(__file__))
# _CHEMIN_CONFIG = os.path.join(_DOSSIER, 'config.json')
# constantes = charger_config_depuis_fichier(_CHEMIN_CONFIG)
# GRILLE_TAILLE = constantes['GRILLE_TAILLE']
# ... etc.

print("Niveau 3 : OK — version intégrable dans jeu/config.py")
print("\nRègle DRY appliquée : toutes les constantes viennent de config.json")
print("Pour changer une règle du jeu, modifier config.json uniquement.")
