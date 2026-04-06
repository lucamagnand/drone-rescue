# =============================================================================
# Corrigé — Module P09 : Assemblage final — main.py
# Fichier cible dans jeu/ : jeu/main.py
# =============================================================================
#
# NIVEAU 1 — Solution minimale (le strict nécessaire pour lancer une partie)
# -----------------------------------------------------------------------------

from logique import initialiser_partie          # noqa: F401 (import conditionnel)
from console import boucle_de_jeu              # noqa: F401
from affichage import render_grille            # noqa: F401
from logger import demarrer_log                # noqa: F401


def main_niveau1():
    """Point d'entrée minimal : démarre et lance la partie."""
    etat = initialiser_partie()
    boucle_de_jeu(etat)


# if __name__ == '__main__':
#     main_niveau1()


# =============================================================================
# NIVEAU 2 — Enrichissement (logger, affichage initial, résultat final)
# -----------------------------------------------------------------------------

def main_niveau2():
    """Point d'entrée enrichi : log, grille initiale, résultat final."""
    demarrer_log()                # initialise le fichier de log
    etat = initialiser_partie()   # construit l'état initial complet
    render_grille(etat)           # affiche la grille de départ
    boucle_de_jeu(etat)           # boucle principale (J1 → J2 → fin_de_tour)

    # Affichage du résultat
    if etat["victoire"]:
        print("\n🏆 Victoire ! Tous les survivants ont été sauvés.")
    else:
        print("\n💀 Défaite. La mission a échoué.")
        print(f"Score final : {etat['score']} point(s) — {etat['tour']} tour(s) joués.")


# if __name__ == '__main__':
#     main_niveau2()


# =============================================================================
# NIVEAU 3 — Version complète intégrable dans jeu/main.py
# -----------------------------------------------------------------------------

def main():
    """
    Point d'entrée principal du jeu Drone Rescue.

    Orchestre dans l'ordre :
    1. Démarrage du logger
    2. Initialisation de la partie (état complet)
    3. Affichage de la grille de départ
    4. Boucle de jeu principale
    5. Affichage du résultat final

    Ne contient aucune logique métier : tout est délégué aux modules.
    """
    demarrer_log()
    print("=" * 50)
    print("       DRONE RESCUE — Mission de sauvetage")
    print("=" * 50)

    etat = initialiser_partie()
    render_grille(etat)

    boucle_de_jeu(etat)

    print("\n" + "=" * 50)
    if etat["victoire"]:
        print("🏆 VICTOIRE ! Tous les survivants ont été sauvés.")
    else:
        print("💀 DÉFAITE. La mission a échoué.")
    print(f"Score final   : {etat['score']} point(s)")
    print(f"Tours joués   : {etat['tour']}")
    drones_hs = sum(
        1 for d in etat["drones"].values() if d.get("hors_service", False)
    )
    print(f"Drones perdus : {drones_hs}")
    print("=" * 50)


if __name__ == '__main__':
    main()
