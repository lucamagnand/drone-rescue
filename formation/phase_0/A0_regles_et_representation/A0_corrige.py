# =============================================================================
# Corrigé — Module A0 : Lire les règles, représenter le jeu
# Fichier cible dans jeu/ : (aucun — module de compréhension)
# =============================================================================

# NIVEAU 1 — Solution minimale (le strict nécessaire pour que ça fonctionne)
# -----------------------------------------------------------------------------

def creer_grille_vide():
    """Crée une grille 12x12 remplie de cases vides '.'"""
    return [['.' for _ in range(12)] for _ in range(12)]


def placer_entite(grille, col, lig, symbole):
    """Place un symbole en (col, lig) sur la grille.

    Args:
        grille (list[list[str]]): la grille 12x12.
        col (int): index de colonne (0 = A, 11 = L).
        lig (int): index de ligne (0 = ligne 1, 11 = ligne 12).
        symbole (str): le symbole à placer.
    """
    grille[lig][col] = symbole


def afficher_grille(grille):
    """Affiche la grille avec en-têtes colonnes (A-L) et numéros de lignes."""
    # En-tête colonnes
    entete = "   " + " ".join(chr(65 + i) for i in range(12))
    print(entete)
    # Lignes
    for lig in range(12):
        num = f"{lig + 1:2d} "
        contenu = " ".join(grille[lig])
        print(num + contenu)


# --- Démonstration niveau 1 ---
if __name__ == "__main__":
    g = creer_grille_vide()
    placer_entite(g, col=0, lig=0, symbole="H")   # Hôpital en A1
    placer_entite(g, col=2, lig=3, symbole="D")   # Drone en C4
    placer_entite(g, col=6, lig=6, symbole="S")   # Survivant en G7
    placer_entite(g, col=9, lig=9, symbole="T")   # Tempête en J10
    afficher_grille(g)


# NIVEAU 2 — Enrichissement (robustesse, cas limites)
# -----------------------------------------------------------------------------

def creer_grille_vide_v2(taille=12):
    """Crée une grille carrée de taille configurable."""
    return [['.' for _ in range(taille)] for _ in range(taille)]


def placer_entite_v2(grille, col, lig, symbole):
    """Place un symbole avec vérification des bornes.

    Raises:
        ValueError: si les coordonnées sont hors grille.
    """
    taille = len(grille)
    if not (0 <= lig < taille and 0 <= col < taille):
        raise ValueError(
            f"Coordonnées ({col}, {lig}) hors grille (taille={taille})"
        )
    grille[lig][col] = symbole


def coord_depuis_chaine(chaine):
    """Convertit une chaîne comme 'C4' en (col, lig) entiers.

    Args:
        chaine (str): coordonnée au format lettre + chiffre(s), ex. 'C4', 'L12'.

    Returns:
        tuple[int, int]: (col, lig) en index 0-basé.

    Raises:
        ValueError: si le format est incorrect.
    """
    chaine = chaine.strip().upper()
    if len(chaine) < 2:
        raise ValueError(f"Coordonnée invalide : '{chaine}'")
    lettre = chaine[0]
    if not lettre.isalpha():
        raise ValueError(f"La colonne doit être une lettre : '{lettre}'")
    col = ord(lettre) - ord('A')
    try:
        lig = int(chaine[1:]) - 1
    except ValueError:
        raise ValueError(f"La ligne doit être un entier : '{chaine[1:]}'")
    return col, lig


# NIVEAU 3 — Version complète intégrable dans jeu/
# (identique à ce que fait affichage.py dans le jeu réel)
# -----------------------------------------------------------------------------

def afficher_grille_complete(etat):
    """Affiche la grille depuis le dictionnaire d'état global.

    Args:
        etat (dict): l'état global de la partie (voir PROMPT_FORMATION.md).
    """
    grille = etat["grille"]
    print()
    entete = "    " + "  ".join(chr(65 + i) for i in range(12))
    print(entete)
    print("   " + "-" * 36)
    for lig in range(12):
        num = f"{lig + 1:2d} |"
        contenu = "  ".join(grille[lig])
        print(num + " " + contenu)
    print()


# --- Test niveau 3 ---
if __name__ == "__main__":
    etat_exemple = {
        "tour": 1,
        "score": 0,
        "partie_finie": False,
        "victoire": False,
        "grille": creer_grille_vide(),
        "hopital": (0, 0),
        "batiments": [],
        "drones": {},
        "tempetes": {},
        "survivants": {},
        "zones_x": set(),
        "historique": [],
    }
    etat_exemple["grille"][0][0] = "H"
    etat_exemple["grille"][3][2] = "D"
    etat_exemple["grille"][6][6] = "S"
    etat_exemple["grille"][9][9] = "T"
    afficher_grille_complete(etat_exemple)
