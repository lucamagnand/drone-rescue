# =============================================================================
# Corrigé — Module P01 : Configuration externe
# Fichier cible dans jeu/ : jeu/config.py + jeu/config.json
# =============================================================================


# NIVEAU 1 — Solution minimale (le strict nécessaire pour que ça fonctionne)
# -----------------------------------------------------------------------------
# On lit config.json avec un chemin relatif simple.
# Fonctionne uniquement si on lance Python depuis le dossier qui contient ce script.

import json

with open("config.json", encoding="utf-8") as _f:
    _cfg = json.load(_f)

# Constantes minimales pour démarrer
GRILLE_TAILLE = _cfg["grille"]["lignes"]
NB_DRONES     = _cfg["drones"]["nb_max_j1"]
BATTERIE_MAX  = _cfg["drones"]["batterie_max"]
BATTERIE_INIT = _cfg["drones"]["batterie_depart"]
NB_TOURS_MAX  = 40  # valeur codée en dur pour l'instant


# NIVEAU 2 — Enrichissement (chemin robuste + toutes les constantes)
# -----------------------------------------------------------------------------
# On utilise os.path pour calculer le chemin absolu à partir de l'emplacement
# de ce script, ce qui rend le code utilisable depuis n'importe quel répertoire.

import json
import os

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
_CHEMIN_CONFIG = os.path.join(_DOSSIER, "config.json")

with open(_CHEMIN_CONFIG, encoding="utf-8") as _f:
    _cfg = json.load(_f)

# Grille
GRILLE_TAILLE = _cfg["grille"]["lignes"]

# Drones
NB_DRONES     = _cfg["drones"]["nb_max_j1"]
BATTERIE_MAX  = _cfg["drones"]["batterie_max"]
BATTERIE_INIT = _cfg["drones"]["batterie_depart"]

# Tempêtes
NB_TEMPETES = _cfg["tempetes"]["nb_max_j2"]
PROB_METEO  = _cfg["tempetes"]["prob_meteo"]

# Règles
COUT_TRANSPORT   = _cfg["regles"]["cout_transport_survivant"]
COUT_ZONE_X      = _cfg["regles"]["cout_entree_zone_x"]
RECHARGE_HOPITAL = _cfg["regles"]["recharge_hopital_par_tour"]

# Constantes non présentes dans JSON (calculées ou fixées)
NB_SURVIVANTS       = 10
NB_BATIMENTS        = 20
NB_ZONES_DANGER     = 2
MAX_DEPL_DRONE      = 3
MAX_DEPL_TEMPETE    = 2
NB_TOURS_MAX        = 40
PROBA_PROPAGATION   = 0.5
PROPAGATION_FREQUENCE = 2


# NIVEAU 3 — Version complète intégrable dans jeu/ (identique au code réel)
# -----------------------------------------------------------------------------
# Version identique à jeu/config.py, avec les lettres et directions exposées.

import json
import os

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
_CHEMIN_CONFIG = os.path.join(_DOSSIER, "config.json")

with open(_CHEMIN_CONFIG, encoding="utf-8") as _f:
    _cfg = json.load(_f)

# ── Grille ───────────────────────────────────────────────────────────────────
GRILLE_TAILLE = _cfg["grille"]["lignes"]

# ── Drones ───────────────────────────────────────────────────────────────────
NB_DRONES     = _cfg["drones"]["nb_max_j1"]
BATTERIE_MAX  = _cfg["drones"]["batterie_max"]
BATTERIE_INIT = _cfg["drones"]["batterie_depart"]

# ── Tempêtes ──────────────────────────────────────────────────────────────────
NB_TEMPETES = _cfg["tempetes"]["nb_max_j2"]
PROB_METEO  = _cfg["tempetes"]["prob_meteo"]

# ── Règles de jeu ─────────────────────────────────────────────────────────────
COUT_TRANSPORT   = _cfg["regles"]["cout_transport_survivant"]
COUT_ZONE_X      = _cfg["regles"]["cout_entree_zone_x"]
RECHARGE_HOPITAL = _cfg["regles"]["recharge_hopital_par_tour"]

# ── Placement initial ─────────────────────────────────────────────────────────
NB_SURVIVANTS       = 10
NB_BATIMENTS        = 20
NB_ZONES_DANGER     = 2

# ── Limites de déplacement par tour ──────────────────────────────────────────
MAX_DEPL_DRONE   = 3
MAX_DEPL_TEMPETE = 2

# ── Tour maximum ─────────────────────────────────────────────────────────────
NB_TOURS_MAX = 40

# ── Propagation des zones X ───────────────────────────────────────────────────
PROBA_PROPAGATION     = 0.5
PROPAGATION_FREQUENCE = 2

# ── Lettres de colonnes ───────────────────────────────────────────────────────
LETTRES = _cfg["lettres"][:GRILLE_TAILLE]

# ── Directions ────────────────────────────────────────────────────────────────
DIRECTIONS = _cfg["directions"]


# -----------------------------------------------------------------------------
# Vérification rapide (à exécuter directement : python P01_corrige.py)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"GRILLE_TAILLE    = {GRILLE_TAILLE}")
    print(f"NB_DRONES        = {NB_DRONES}")
    print(f"BATTERIE_MAX     = {BATTERIE_MAX}")
    print(f"NB_TOURS_MAX     = {NB_TOURS_MAX}")
    print(f"LETTRES          = {LETTRES}")
    print(f"DIRECTIONS       = {DIRECTIONS}")
    print("✅ config.py chargé avec succès.")
