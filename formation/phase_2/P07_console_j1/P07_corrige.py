# =============================================================================
# Corrigé — Module P07 : Console J1 (saisie, parsing, validation, exécution)
# Fichier cible dans jeu/ : jeu/console.py — fonction phase_j1(etat)
# =============================================================================

COLS = 'ABCDEFGHIJKL'
MAX_DEPLACEMENTS_J1 = 3


# NIVEAU 1 — Solution minimale (parser seul)
# -----------------------------------------------------------------------------

def position_depuis_chaine(chaine):
    """
    Convertit une notation humaine (ex : 'B4') en indices (col, lig).
    Retourne (None, None) si le format est invalide.
    """
    try:
        col = COLS.index(chaine[0].upper())
        lig = int(chaine[1:]) - 1
        if 0 <= col < 12 and 0 <= lig < 12:
            return col, lig
    except (ValueError, IndexError):
        pass
    return None, None


# NIVEAU 2 — Enrichissement (boucle complète avec gestion d'erreurs)
# -----------------------------------------------------------------------------

def phase_j1_v2(etat, valider_mouvement, executer_mouvement, input_fn=input):
    """
    Phase J1 : boucle de saisie avec validation et exécution.
    input_fn injectable pour les tests (remplace input()).
    """
    nb_depl = 0
    logs = []

    while nb_depl < MAX_DEPLACEMENTS_J1:
        saisie = input_fn(f"  J1 [{nb_depl}/{MAX_DEPLACEMENTS_J1}] > ").strip()

        if saisie.lower() in ("fin", "passe", ""):
            break

        parties = saisie.split()
        if len(parties) != 2:
            print("  Format attendu : D1 B4")
            continue

        id_drone, pos_str = parties[0].upper(), parties[1]

        if id_drone not in etat["drones"]:
            print(f"  Drone {id_drone} inconnu.")
            continue

        col, lig = position_depuis_chaine(pos_str)
        if col is None:
            print(f"  Position '{pos_str}' invalide. Exemple : B4")
            continue

        ok, msg = valider_mouvement(etat, id_drone, col, lig)
        if not ok:
            print(f"  Mouvement refusé : {msg}")
            continue

        log = executer_mouvement(etat, id_drone, col, lig)
        print(f"  ✓ {log}")
        logs.append(log)
        nb_depl += 1

    return logs


# NIVEAU 3 — Version complète intégrable dans jeu/console.py
# -----------------------------------------------------------------------------

def phase_j1(etat, valider_fn, executer_fn):
    """
    Tour complet de J1 : jusqu'à MAX_DEPLACEMENTS_J1 déplacements.
    Saisie format 'D1 B4' ou 'fin'/'passe' pour terminer.
    Loggue chaque action dans etat['historique'].

    Args:
        etat : dict — état global du jeu
        valider_fn : callable — valider_mouvement(etat, id, col, lig)
        executer_fn : callable — executer_mouvement(etat, id, col, lig)
    """
    nb_depl = 0
    print(f"\n=== Tour {etat['tour']} — J1 (max {MAX_DEPLACEMENTS_J1} déplacements) ===")

    while nb_depl < MAX_DEPLACEMENTS_J1:
        try:
            saisie = input(f"  J1 [{nb_depl}/{MAX_DEPLACEMENTS_J1}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if saisie.lower() in ("fin", "passe", ""):
            break

        parties = saisie.split()
        if len(parties) != 2:
            print("  Format : D1 B4  |  'fin' pour terminer")
            continue

        id_drone, pos_str = parties[0].upper(), parties[1]

        if id_drone not in etat["drones"]:
            print(f"  Drone '{id_drone}' inconnu. Drones disponibles : "
                  + ", ".join(etat["drones"].keys()))
            continue

        col, lig = position_depuis_chaine(pos_str)
        if col is None:
            print(f"  Position '{pos_str}' invalide. Exemple : B4 (colonne B, ligne 4)")
            continue

        ok, msg = valider_fn(etat, id_drone, col, lig)
        if not ok:
            print(f"  ✗ Refusé : {msg}")
            continue

        log = executer_fn(etat, id_drone, col, lig)
        print(f"  ✓ {log}")
        etat["historique"].append(f"J1 | {log}")
        nb_depl += 1

    print(f"  → J1 : {nb_depl} déplacement(s) effectué(s)")


# --- Tests rapides ---
if __name__ == "__main__":
    # Vérification du parser
    assert position_depuis_chaine("A1") == (0, 0)
    assert position_depuis_chaine("B4") == (1, 3)
    assert position_depuis_chaine("L12") == (11, 11)
    assert position_depuis_chaine("Z9") == (None, None)
    assert position_depuis_chaine("") == (None, None)
    print("Tests parser OK")
