# =============================================================================
# Corrigé — Module P02 : Entités et initialisation
# Fichier cible dans jeu/ : jeu/logique.py
#   Fonctions : creer_drone(), creer_survivant(), creer_tempete(),
#               initialiser_partie()
# =============================================================================


# NIVEAU 1 — Solution minimale (le strict nécessaire pour que ça fonctionne)
# -----------------------------------------------------------------------------
# Constantes codées en dur pour ne pas dépendre de config.py dans ce niveau.

BATTERIE_INIT_N1 = 10
BATTERIE_MAX_N1  = 20

def creer_drone_n1(identifiant, col, lig):
    """Factory minimale — crée un drone avec les attributs essentiels."""
    return {
        "id"       : identifiant,
        "col"      : col,
        "lig"      : lig,
        "batterie" : BATTERIE_INIT_N1,
        "survivant": None,
        "bloque"   : 0,
        "hors_service": False,
    }

def creer_survivant_n1(identifiant, col, lig):
    """Factory minimale — crée un survivant en attente."""
    return {"id": identifiant, "col": col, "lig": lig, "etat": "en_attente"}

def creer_tempete_n1(identifiant, col, lig):
    """Factory minimale — crée une tempête avec direction fixe (vers la droite)."""
    return {"id": identifiant, "col": col, "lig": lig, "dx": 1, "dy": 0}


# NIVEAU 2 — Enrichissement (robustesse, batterie_max, direction aléatoire tempête)
# -----------------------------------------------------------------------------

import random

# Constantes (en production, ces valeurs viennent de config.py)
BATTERIE_INIT = 10
BATTERIE_MAX  = 20
GRILLE_TAILLE = 12

def creer_drone(identifiant, col, lig):
    """Retourne un dictionnaire représentant un drone."""
    return {
        "id"          : identifiant,
        "col"         : col,
        "lig"         : lig,
        "batterie"    : BATTERIE_INIT,
        "batterie_max": BATTERIE_MAX,
        "survivant"   : None,
        "bloque"      : 0,
        "hors_service": False,
    }

def creer_survivant(identifiant, col, lig):
    """Retourne un dictionnaire représentant un survivant."""
    return {"id": identifiant, "col": col, "lig": lig, "etat": "en_attente"}

def creer_tempete(identifiant, col, lig):
    """
    Retourne un dictionnaire représentant une tempête.
    La direction initiale (dx, dy) est aléatoire, mais ne peut pas être (0, 0).
    """
    dx = random.choice([-1, 0, 1])
    dy = random.choice([-1, 0, 1])
    if dx == 0 and dy == 0:
        dx = 1  # garantit qu'une tempête se déplace toujours
    return {"id": identifiant, "col": col, "lig": lig, "dx": dx, "dy": dy}


def _position_aleatoire(occupees, interdites=None, max_tentatives=200):
    """Retourne une position (col, lig) aléatoire non occupée."""
    interdit = (interdites or set()) | occupees
    for _ in range(max_tentatives):
        col = random.randint(0, GRILLE_TAILLE - 1)
        lig = random.randint(0, GRILLE_TAILLE - 1)
        pos = (col, lig)
        if pos not in interdit:
            return pos
    return None  # impossible de placer : grille trop remplie


def initialiser_partie_n2():
    """
    Crée un état minimal : hôpital + 2 drones + 2 tempêtes + 3 survivants.
    Pas de bâtiments ni de zones X dans cette version simplifiée.
    """
    occupees = set()
    grille = [['.' for _ in range(GRILLE_TAILLE)] for _ in range(GRILLE_TAILLE)]

    # Hôpital
    hopital = _position_aleatoire(occupees)
    occupees.add(hopital)
    grille[hopital[1]][hopital[0]] = 'H'

    # Drones
    drones = {}
    for i in range(1, 3):
        pos = _position_aleatoire(occupees)
        did = f"D{i}"
        drones[did] = creer_drone(did, pos[0], pos[1])
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'D'

    # Tempêtes
    tempetes = {}
    for i in range(1, 3):
        pos = _position_aleatoire(occupees)
        tid = f"T{i}"
        tempetes[tid] = creer_tempete(tid, pos[0], pos[1])
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'T'

    # Survivants
    survivants = {}
    for i in range(1, 4):
        pos = _position_aleatoire(occupees)
        sid = f"S{i}"
        survivants[sid] = creer_survivant(sid, pos[0], pos[1])
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'S'

    return {
        "tour"        : 1,
        "score"       : 0,
        "partie_finie": False,
        "victoire"    : False,
        "grille"      : grille,
        "hopital"     : hopital,
        "batiments"   : [],
        "drones"      : drones,
        "tempetes"    : tempetes,
        "survivants"  : survivants,
        "zones_x"     : set(),
        "historique"  : [],
    }


# NIVEAU 3 — Version complète intégrable dans jeu/ (identique au code réel)
# -----------------------------------------------------------------------------
# Cette version importe les constantes depuis config.py et gère tous
# les éléments : bâtiments, zones X, voisins interdits autour de l'hôpital.

import random

# En production : from config import (
#     GRILLE_TAILLE, NB_DRONES, NB_TEMPETES, NB_BATIMENTS, NB_SURVIVANTS,
#     BATTERIE_MAX, BATTERIE_INIT, NB_ZONES_DANGER )

# Pour que ce fichier soit exécutable seul :
GRILLE_TAILLE = 12
NB_DRONES     = 6
NB_TEMPETES   = 4
NB_BATIMENTS  = 20
NB_SURVIVANTS = 10
BATTERIE_MAX  = 20
BATTERIE_INIT = 10
NB_ZONES_DANGER = 2


def creer_drone(identifiant, col, lig):
    """Retourne un dictionnaire représentant un drone."""
    return {
        "id"          : identifiant,
        "col"         : col,
        "lig"         : lig,
        "batterie"    : BATTERIE_INIT,
        "batterie_max": BATTERIE_MAX,
        "survivant"   : None,
        "bloque"      : 0,
        "hors_service": False,
    }


def creer_survivant(identifiant, col, lig):
    """Retourne un dictionnaire représentant un survivant."""
    return {"id": identifiant, "col": col, "lig": lig, "etat": "en_attente"}


def creer_tempete(identifiant, col, lig):
    """Retourne un dictionnaire représentant une tempête."""
    dx = random.choice([-1, 0, 1])
    dy = random.choice([-1, 0, 1])
    if dx == 0 and dy == 0:
        dx = 1
    return {"id": identifiant, "col": col, "lig": lig, "dx": dx, "dy": dy}


def _voisins_diag(pos):
    """Retourne les 8 voisins (diagonales incluses) d'une position."""
    col, lig = pos
    return [
        (col + dc, lig + dl)
        for dc in (-1, 0, 1)
        for dl in (-1, 0, 1)
        if not (dc == 0 and dl == 0)
    ]


def _position_aleatoire(occupees, interdites=None, max_tentatives=200):
    """Retourne une position (col, lig) aléatoire non occupée et non interdite."""
    interdit = (interdites or set()) | occupees
    for _ in range(max_tentatives):
        col = random.randint(0, GRILLE_TAILLE - 1)
        lig = random.randint(0, GRILLE_TAILLE - 1)
        pos = (col, lig)
        if pos not in interdit:
            return pos
    return None


def initialiser_partie():
    """
    Crée et retourne un état de jeu complet (dictionnaire).
    Placement aléatoire de toutes les entités sans chevauchement.
    L'hôpital est protégé : aucun bâtiment dans ses 8 cases adjacentes.
    """
    occupees = set()
    grille = [['.' for _ in range(GRILLE_TAILLE)] for _ in range(GRILLE_TAILLE)]

    # Hôpital
    hopital = _position_aleatoire(occupees)
    occupees.add(hopital)
    grille[hopital[1]][hopital[0]] = 'H'

    # Cases interdites aux bâtiments (8 voisins de l'hôpital)
    interdites_bat = set(_voisins_diag(hopital))

    # Bâtiments
    batiments = []
    for _ in range(NB_BATIMENTS):
        pos = _position_aleatoire(occupees, interdites=interdites_bat)
        if pos is None:
            break
        batiments.append(pos)
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'B'

    # Drones
    drones = {}
    for i in range(1, NB_DRONES + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        did = f"D{i}"
        drones[did] = creer_drone(did, pos[0], pos[1])
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'D'

    # Tempêtes
    tempetes = {}
    for i in range(1, NB_TEMPETES + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        tid = f"T{i}"
        tempetes[tid] = creer_tempete(tid, pos[0], pos[1])
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'T'

    # Survivants
    survivants = {}
    for i in range(1, NB_SURVIVANTS + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        sid = f"S{i}"
        survivants[sid] = creer_survivant(sid, pos[0], pos[1])
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'S'

    # Zones X
    zones_x = set()
    for _ in range(NB_ZONES_DANGER):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        zones_x.add(pos)
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'X'

    return {
        "tour"        : 1,
        "score"       : 0,
        "partie_finie": False,
        "victoire"    : False,
        "grille"      : grille,
        "hopital"     : hopital,
        "batiments"   : batiments,
        "drones"      : drones,
        "tempetes"    : tempetes,
        "survivants"  : survivants,
        "zones_x"     : zones_x,
        "historique"  : [],
    }


# -----------------------------------------------------------------------------
# Vérification rapide
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    etat = initialiser_partie()
    print(f"Tour          : {etat['tour']}")
    print(f"Hôpital       : {etat['hopital']}")
    print(f"Drones        : {list(etat['drones'].keys())}")
    print(f"Tempêtes      : {list(etat['tempetes'].keys())}")
    print(f"Survivants    : {list(etat['survivants'].keys())}")
    print(f"Bâtiments     : {len(etat['batiments'])} placés")
    print(f"Zones X       : {etat['zones_x']}")
    # Vérifications d'intégrité
    assert etat['tour'] == 1
    assert isinstance(etat['grille'], list) and len(etat['grille']) == GRILLE_TAILLE
    assert isinstance(etat['zones_x'], set)
    for did, d in etat['drones'].items():
        assert 'batterie' in d and 'bloque' in d and 'hors_service' in d, \
            f"Attribut manquant dans {did}"
    print("✅ initialiser_partie() validée.")
