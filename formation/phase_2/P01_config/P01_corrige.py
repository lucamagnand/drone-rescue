# =============================================================================
# Corrigé — Module P01 : config.py
# Fichier cible dans jeu/ : jeu/config.py + jeu/config.json
# =============================================================================
#
# NIVEAU 1 — Solution minimale
# -----------------------------------------------------------------------------
import json

# Simulation de config.json (en production, lire depuis le fichier)
CONFIG_JSON = {
    "GRILLE_TAILLE": 12,
    "BATTERIE_MAX": 20,
    "NB_DRONES": 2,
    "MAX_TOURS": 30,
    "MAX_DEPL_J1": 3,
    "MAX_DEPL_J2": 2,
    "NB_SURVIVANTS": 3,
    "PROPAGATION_TOURS": 5,
    "PROBA_PROPAGATION": 0.3,
    "HOPITAL_COL": 0,
    "HOPITAL_LIG": 0,
}


def charger_config_v1(config_dict):
    """Charge la configuration depuis un dict et retourne les constantes."""
    return {
        "GRILLE_TAILLE":    config_dict.get("GRILLE_TAILLE", 12),
        "BATTERIE_MAX":     config_dict.get("BATTERIE_MAX", 20),
        "NB_DRONES":        config_dict.get("NB_DRONES", 2),
        "MAX_TOURS":        config_dict.get("MAX_TOURS", 30),
        "MAX_DEPL_J1":      config_dict.get("MAX_DEPL_J1", 3),
        "MAX_DEPL_J2":      config_dict.get("MAX_DEPL_J2", 2),
        "NB_SURVIVANTS":    config_dict.get("NB_SURVIVANTS", 3),
        "PROPAGATION_TOURS": config_dict.get("PROPAGATION_TOURS", 5),
        "PROBA_PROPAGATION": config_dict.get("PROBA_PROPAGATION", 0.3),
        "HOPITAL_COL":      config_dict.get("HOPITAL_COL", 0),
        "HOPITAL_LIG":      config_dict.get("HOPITAL_LIG", 0),
    }


cst = charger_config_v1(CONFIG_JSON)
GRILLE_TAILLE = cst["GRILLE_TAILLE"]
BATTERIE_MAX  = cst["BATTERIE_MAX"]
print(f"Config chargée : grille {GRILLE_TAILLE}x{GRILLE_TAILLE}, batterie_max={BATTERIE_MAX}")


# NIVEAU 2 — Enrichissement : lecture réelle depuis fichier + validation
# -----------------------------------------------------------------------------
import os


def charger_config_fichier(chemin):
    """Lit config.json depuis le système de fichiers.

    Args:
        chemin (str): chemin absolu ou relatif vers config.json.

    Returns:
        dict: constantes de configuration.

    Raises:
        SystemExit: si le fichier est manquant ou mal formé.
    """
    try:
        with open(chemin, encoding="utf-8") as f:
            donnees = json.load(f)
    except FileNotFoundError:
        print(f"ERREUR : config.json introuvable à {chemin}")
        raise SystemExit(1)
    except json.JSONDecodeError as e:
        print(f"ERREUR : config.json mal formé — {e}")
        raise SystemExit(1)
    return charger_config_v1(donnees)


# NIVEAU 3 — Version intégrable dans jeu/config.py
# -----------------------------------------------------------------------------

# En production, ce module est importé par tous les autres :
#   from config import GRILLE_TAILLE, BATTERIE_MAX, MAX_DEPL_J1
#
# Structure réelle de jeu/config.py :
#
#   import json, os
#   _DIR = os.path.dirname(os.path.abspath(__file__))
#   _PATH = os.path.join(_DIR, 'config.json')
#   with open(_PATH, encoding='utf-8') as f:
#       _C = json.load(f)
#   GRILLE_TAILLE   = _C.get('GRILLE_TAILLE', 12)
#   BATTERIE_MAX    = _C.get('BATTERIE_MAX', 20)
#   NB_DRONES       = _C.get('NB_DRONES', 2)
#   MAX_TOURS       = _C.get('MAX_TOURS', 30)
#   MAX_DEPL_J1     = _C.get('MAX_DEPL_J1', 3)
#   MAX_DEPL_J2     = _C.get('MAX_DEPL_J2', 2)
#   NB_SURVIVANTS   = _C.get('NB_SURVIVANTS', 3)
#   HOPITAL_COL     = _C.get('HOPITAL_COL', 0)
#   HOPITAL_LIG     = _C.get('HOPITAL_LIG', 0)

if __name__ == "__main__":
    print("\n--- Test P01 ---")
    c = charger_config_v1(CONFIG_JSON)
    assert c["GRILLE_TAILLE"] == 12
    assert c["BATTERIE_MAX"] == 20
    assert c["MAX_DEPL_J1"] == 3
    print("✅ Config chargée et validée")
