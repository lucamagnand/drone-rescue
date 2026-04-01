# =============================================================================
# Corrigé — Module P08 : Console J2 et boucle de jeu
# Fichier cible dans jeu/ : jeu/console.py — phase_j2(), boucle_de_jeu()
# =============================================================================

import random

COLS = 'ABCDEFGHIJKL'
MAX_DEPLACEMENTS_J2 = 2
GRILLE_TAILLE = 12


def position_depuis_chaine(chaine):
    """Convertit 'B4' en (col=1, lig=3). Retourne (None, None) si invalide."""
    try:
        col = COLS.index(chaine[0].upper())
        lig = int(chaine[1:]) - 1
        if 0 <= col < 12 and 0 <= lig < 12:
            return col, lig
    except (ValueError, IndexError):
        pass
    return None, None


# NIVEAU 1 — Validation du mouvement d'une tempête
# -----------------------------------------------------------------------------

def valider_mouvement_tempete(etat, id_tempete, col_cible, lig_cible):
    """
    Vérifie que le déplacement de la tempête est légal :
    - la tempête existe
    - la case cible est dans la grille
    - la distance de Chebyshev est <= 1
    Retourne (bool, str).
    """
    t = etat["tempetes"].get(id_tempete)
    if t is None:
        return False, f"{id_tempete} inconnue"
    if not (0 <= col_cible < GRILLE_TAILLE and 0 <= lig_cible < GRILLE_TAILLE):
        return False, "hors grille"
    dist = max(abs(col_cible - t["col"]), abs(lig_cible - t["lig"]))
    if dist > 1:
        return False, f"distance {dist} > 1 case autorisée"
    return True, "ok"


# NIVEAU 2 — Phase J2 complète
# -----------------------------------------------------------------------------

def phase_j2(etat, input_fn=input):
    """
    Tour de J2 : jusqu'à MAX_DEPLACEMENTS_J2 déplacements de tempêtes.
    Saisie : 'T1 F6' ou 'fin'/'passe' pour terminer.
    input_fn injectable pour les tests.
    """
    nb_depl = 0
    logs = []

    while nb_depl < MAX_DEPLACEMENTS_J2:
        try:
            saisie = input_fn(f"  J2 [{nb_depl}/{MAX_DEPLACEMENTS_J2}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if saisie.lower() in ("fin", "passe", ""):
            break

        parties = saisie.split()
        if len(parties) != 2:
            print("  Format : T1 F6  |  'fin' pour terminer")
            continue

        id_tempete, pos_str = parties[0].upper(), parties[1]

        if id_tempete not in etat["tempetes"]:
            print(f"  Tempête '{id_tempete}' inconnue. "
                  f"Tempêtes disponibles : {', '.join(etat['tempetes'].keys())}")
            continue

        col, lig = position_depuis_chaine(pos_str)
        if col is None:
            print(f"  Position '{pos_str}' invalide. Exemple : F6")
            continue

        ok, msg = valider_mouvement_tempete(etat, id_tempete, col, lig)
        if not ok:
            print(f"  ✗ Refusé : {msg}")
            continue

        # Exécution du déplacement
        t = etat["tempetes"][id_tempete]
        etat["grille"][t["lig"]][t["col"]] = "."
        t["col"], t["lig"] = col, lig
        etat["grille"][lig][col] = id_tempete
        log = f"{id_tempete} → ({col},{lig})"
        print(f"  ✓ {log}")
        etat["historique"].append(f"J2 | {log}")
        logs.append(log)
        nb_depl += 1

    return logs


# NIVEAU 3 — Boucle de jeu complète intégrable dans jeu/console.py
# -----------------------------------------------------------------------------

def deplacer_tempetes(etat):
    """Phase météo : chaque tempête bouge avec 50% de chance."""
    for tid, t in etat["tempetes"].items():
        if random.random() < 0.5:
            etat["grille"][t["lig"]][t["col"]] = "."
            t["col"] = max(0, min(GRILLE_TAILLE - 1, t["col"] + t["dx"]))
            t["lig"] = max(0, min(GRILLE_TAILLE - 1, t["lig"] + t["dy"]))
            etat["grille"][t["lig"]][t["col"]] = tid


def verifier_fin_partie(etat, TOURS_MAX=50):
    """Vérifie les 3 conditions de fin de partie."""
    if all(s["etat"] == "sauve" for s in etat["survivants"].values()):
        etat["partie_finie"] = True
        etat["victoire"] = True
        return "Victoire ! Tous les survivants sont en sécurité."
    if all(d["hors_service"] for d in etat["drones"].values()):
        etat["partie_finie"] = True
        etat["victoire"] = False
        return "Défaite — tous les drones sont hors service."
    if etat["tour"] >= TOURS_MAX:
        etat["partie_finie"] = True
        etat["victoire"] = False
        return f"Défaite — {TOURS_MAX} tours dépassés."
    return ""


def boucle_de_jeu(etat, phase_j1_fn, phase_j2_fn=None,
                  TOURS_MAX=50):
    """
    Orchestre le jeu tour après tour :
      1. phase_j1_fn(etat) — drones
      2. phase_j2_fn(etat) — tempêtes (optionnel)
      3. deplacer_tempetes(etat) — météo automatique
      4. verifier_fin_partie() — conditions de fin
      5. etat['tour'] += 1

    phase_j2_fn peut être None pour un mode solo (J2 IA).
    """
    if phase_j2_fn is None:
        def phase_j2_fn(e):
            """J2 automatique : passe toujours."""
            return []

    while not etat["partie_finie"]:
        print(f"\n{'='*40}")
        print(f"Tour {etat['tour']}  |  Score : {etat['score']}")
        print(f"{'='*40}")

        # 1. Phase J1 — drones
        phase_j1_fn(etat)
        if etat["partie_finie"]:
            break

        # 2. Phase J2 — tempêtes
        phase_j2_fn(etat)
        if etat["partie_finie"]:
            break

        # 3. Phase météo automatique
        deplacer_tempetes(etat)

        # 4. Vérification fin de partie (AVANT incrémentation)
        msg_fin = verifier_fin_partie(etat, TOURS_MAX)

        # 5. Incrémentation du tour
        etat["tour"] += 1

        if msg_fin:
            print(f"\n{'='*40}")
            print(msg_fin)
            print(f"Score final : {etat['score']}")
            break


# --- Tests rapides ---
if __name__ == "__main__":
    random.seed(42)

    # Construction d'état minimal
    grille = [["." for _ in range(12)] for _ in range(12)]
    etat = {
        "tour": 1, "score": 0, "partie_finie": False, "victoire": False,
        "grille": grille, "hopital": (0, 0), "batiments": [],
        "drones": {
            "D1": {"id": "D1", "col": 3, "lig": 3, "batterie": 15,
                   "batterie_max": 20, "survivant": None,
                   "bloque": 0, "hors_service": False}
        },
        "tempetes": {
            "T1": {"id": "T1", "col": 5, "lig": 5, "dx": 1, "dy": 0}
        },
        "survivants": {
            "S1": {"id": "S1", "col": 4, "lig": 4, "etat": "en_attente"}
        },
        "zones_x": set(), "historique": []
    }
    etat["grille"][0][0] = "H"
    etat["grille"][3][3] = "D1"
    etat["grille"][5][5] = "T1"
    etat["grille"][4][4] = "S1"

    # Test validation tempête
    ok, _ = valider_mouvement_tempete(etat, "T1", 6, 5)
    assert ok, "Déplacement adjacent valide"
    ok2, _ = valider_mouvement_tempete(etat, "T1", 9, 5)
    assert not ok2, "Distance 4 invalide"
    print("Tests validation tempête OK")

    # Test boucle : fin par tours max
    boucle_de_jeu(etat,
                  phase_j1_fn=lambda e: None,
                  phase_j2_fn=lambda e: None,
                  TOURS_MAX=3)
    assert etat["partie_finie"]
    print("Test boucle de jeu OK")
