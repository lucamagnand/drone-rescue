# =============================================================================
# Corrigé — Module P03 : Affichage
# Fichier cible dans jeu/ : jeu/affichage.py
#   Fonction principale : render_grille(etat)
# =============================================================================


# NIVEAU 1 — Solution minimale (affichage brut sans en-têtes)
# -----------------------------------------------------------------------------

def render_grille_n1(etat):
    """Affiche la grille sans en-têtes ni alignement."""
    grille = etat["grille"]
    for lig in range(len(grille)):
        print(" ".join(grille[lig]))
    print()


# Exemple d'utilisation niveau 1 :
# etat_exemple = {
#     "grille": [
#         ['H', '.', '.', '.'],
#         ['.', 'D', '.', '.'],
#         ['.', '.', 'S', '.'],
#         ['.', '.', '.', 'T'],
#     ]
# }
# render_grille_n1(etat_exemple)
# Sortie :
# H . . .
# . D . .
# . . S .
# . . . T


# NIVEAU 2 — Enrichissement (en-têtes colonnes A–L, numéros de lignes)
# -----------------------------------------------------------------------------

COLS = "ABCDEFGHIJKL"

def render_grille_n2(etat):
    """
    Affiche la grille avec en-têtes de colonnes (A–L)
    et numéros de lignes (1–12).
    """
    grille = etat["grille"]
    taille = len(grille)

    # En-tête des colonnes
    en_tete = "     " + "  ".join(COLS[:taille])
    print(en_tete)
    print("     " + "-" * (taille * 3 - 1))

    for lig in range(taille):
        num = str(lig + 1).rjust(2)         # numéro aligné sur 2 caractères
        cases = "  ".join(grille[lig])       # cases séparées par 2 espaces
        print(f"{num} | {cases}")

    print()


# NIVEAU 3 — Version complète intégrable dans jeu/ (avec score, tour, ANSI)
# -----------------------------------------------------------------------------

# Codes couleur ANSI — fonctionnent dans la plupart des terminaux
# (et dans Google Colab). Désactivables en passant COULEURS=False.

COULEURS = True

COULEUR = {
    'H': '\033[92m',   # vert vif — hôpital
    'D': '\033[94m',   # bleu    — drone
    'T': '\033[91m',   # rouge   — tempête
    'S': '\033[93m',   # jaune   — survivant
    'B': '\033[90m',   # gris    — bâtiment
    'X': '\033[95m',   # magenta — zone danger
    '.': '',           # pas de couleur pour les cases vides
}
RESET = '\033[0m'


def _colorier(symbole):
    """Applique une couleur ANSI au symbole si COULEURS est activé."""
    if not COULEURS:
        return symbole
    couleur = COULEUR.get(symbole, '')
    if couleur:
        return f"{couleur}{symbole}{RESET}"
    return symbole


def render_grille(etat):
    """
    Affiche la grille complète en terminal :
    - En-têtes de colonnes (A–L)
    - Numéros de lignes (1–12)
    - Symboles colorés (codes ANSI)
    - Tour et score en en-tête
    """
    grille = etat["grille"]
    taille = len(grille)

    tour   = etat.get("tour", "?")
    score  = etat.get("score", 0)
    nb_surv_sauves = sum(
        1 for s in etat.get("survivants", {}).values()
        if s["etat"] == "sauve"
    )
    nb_surv_total  = len(etat.get("survivants", {}))

    # Bandeau d'info
    print(f"\n  Tour {tour}   Score : {score}   Survivants sauvés : {nb_surv_sauves}/{nb_surv_total}")
    print()

    # En-tête des colonnes
    en_tete = "     " + "  ".join(COLS[:taille])
    print(en_tete)
    separateur = "     " + "-" * (taille * 3 - 1)
    print(separateur)

    for lig in range(taille):
        num   = str(lig + 1).rjust(2)
        cases = "  ".join(_colorier(grille[lig][col]) for col in range(taille))
        print(f"{num} | {cases}")

    print()


# -----------------------------------------------------------------------------
# Vérification rapide
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import random

    GRILLE_TAILLE = 12

    # État minimal de démonstration
    grille = [['.' for _ in range(GRILLE_TAILLE)] for _ in range(GRILLE_TAILLE)]
    grille[0][2]  = 'H'
    grille[3][5]  = 'D'
    grille[7][1]  = 'D'
    grille[5][9]  = 'T'
    grille[2][7]  = 'S'
    grille[9][4]  = 'B'

    etat = {
        "tour"      : 1,
        "score"     : 0,
        "grille"    : grille,
        "survivants": {"S1": {"etat": "en_attente"}, "S2": {"etat": "sauve"}},
    }

    # Test niveau 1
    print("=== Niveau 1 (sans en-têtes) ===")
    render_grille_n1(etat)

    # Test niveau 2
    print("=== Niveau 2 (avec en-têtes) ===")
    render_grille_n2(etat)

    # Test niveau 3
    print("=== Niveau 3 (complet + couleurs) ===")
    render_grille(etat)

    # Vérification sans effet de bord
    import copy
    etat_avant = copy.deepcopy(etat)
    render_grille(etat)
    assert etat["grille"] == etat_avant["grille"], "render_grille() a modifié la grille !"
    print("✅ render_grille() sans effet de bord validé.")
