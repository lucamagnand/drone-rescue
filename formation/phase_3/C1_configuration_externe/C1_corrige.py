# =============================================================================
# Corrigé — Module C1 : Configuration externe
# Fichier cible dans jeu/ : jeu/config.json + jeu/config.py
# =============================================================================
#
# NIVEAU 1 — Identifier les valeurs magiques et les nommer
# -----------------------------------------------------------------------------

# Valeurs magiques trouvées dans le code initial et leurs constantes
VALEURS_MAGIQUES = [
    (12,  'GRILLE_TAILLE',         'Taille de la grille (12×12)'),
    (3,   'NB_DRONES',             'Nombre de drones initiaux'),
    (20,  'BATTERIE_MAX',          'Batterie maximale d\'un drone'),
    (30,  'TOURS_MAX',             'Nombre maximum de tours de jeu'),
    (1,   'DISTANCE_MAX_DEPLACEMENT', 'Distance max de déplacement (Chebyshev)'),
]

print("Valeurs magiques identifiées :")
for valeur, nom, description in VALEURS_MAGIQUES:
    print(f"  {valeur:4} → {nom:30s}  ({description})")


# =============================================================================
# NIVEAU 2 — Simuler config.json et config.py
# -----------------------------------------------------------------------------

import json  # noqa: E402

# Simulation du contenu de config.json
_CONFIG_JSON_CONTENU = """{
  "grille_taille": 12,
  "batterie_max": 20,
  "nb_drones": 3,
  "nb_survivants": 4,
  "nb_tempetes": 2,
  "tours_max": 30,
  "max_deplacements_j1": 3,
  "max_deplacements_j2": 2,
  "cout_batterie_base": 1,
  "cout_batterie_zone_x": 2,
  "recharge_stationnaire": 3,
  "proba_meteo": 0.5
}"""

# Chargement (une seule fois au démarrage)
_cfg = json.loads(_CONFIG_JSON_CONTENU)

# Constantes exposées
GRILLE_TAILLE           = _cfg["grille_taille"]
BATTERIE_MAX            = _cfg["batterie_max"]
NB_DRONES               = _cfg["nb_drones"]
NB_SURVIVANTS           = _cfg["nb_survivants"]
NB_TEMPETES             = _cfg["nb_tempetes"]
TOURS_MAX               = _cfg["tours_max"]
MAX_DEPLACEMENTS_J1     = _cfg["max_deplacements_j1"]
MAX_DEPLACEMENTS_J2     = _cfg["max_deplacements_j2"]
COUT_BATTERIE_BASE      = _cfg["cout_batterie_base"]
COUT_BATTERIE_ZONE_X    = _cfg["cout_batterie_zone_x"]
RECHARGE_STATIONNAIRE   = _cfg["recharge_stationnaire"]
PROBA_METEO             = _cfg["proba_meteo"]


# =============================================================================
# NIVEAU 3 — Version complète de config.py intégrable dans jeu/
# -----------------------------------------------------------------------------

def valider_config(cfg: dict) -> None:
    """
    Vérifie que toutes les clés requises sont présentes dans la configuration.
    Lève une KeyError explicite si une clé manque.

    Args:
        cfg (dict): dictionnaire de configuration chargé depuis config.json

    Raises:
        KeyError: si une clé requise est absente
    """
    cles_requises = [
        "grille_taille", "batterie_max", "nb_drones", "nb_survivants",
        "nb_tempetes", "tours_max", "max_deplacements_j1", "max_deplacements_j2",
        "cout_batterie_base", "cout_batterie_zone_x", "recharge_stationnaire",
        "proba_meteo",
    ]
    for cle in cles_requises:
        if cle not in cfg:
            raise KeyError(
                f"Clé manquante dans config.json : '{cle}'.\n"
                f"Clés présentes : {list(cfg.keys())}"
            )


valider_config(_cfg)
print(f"Config valide : grille {GRILLE_TAILLE}×{GRILLE_TAILLE}, "
      f"{NB_DRONES} drones, {TOURS_MAX} tours max.")
