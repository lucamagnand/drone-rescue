# =============================================================================
# B1_corrige.py — Simuler des fonctions à la main
# Trois niveaux de maîtrise
# =============================================================================

LETTRES = "ABCDEFGHIJKL"  # 12 lettres : A=0, B=1, ..., L=11


def position_depuis_chaine(chaine):
    """Convertit 'B3' en (col=1, lig=2)."""
    lettre = chaine[0]
    num    = int(chaine[1:])
    col    = LETTRES.index(lettre)
    lig    = num - 1
    return (col, lig)


def chaine_depuis_position(col, lig):
    """Convertit (col=1, lig=2) en 'B3'."""
    return f"{LETTRES[col]}{lig + 1}"


def distance_chebyshev(col1, lig1, col2, lig2):
    """Distance de Chebyshev entre deux cases."""
    return max(abs(col2 - col1), abs(lig2 - lig1))


# -----------------------------------------------------------------------------
# NIVEAU 1 — Valeurs attendues (exercice 1)
# -----------------------------------------------------------------------------

assert position_depuis_chaine('A1')  == (0, 0)
assert position_depuis_chaine('B3')  == (1, 2)
assert position_depuis_chaine('L12') == (11, 11)
assert position_depuis_chaine('F6')  == (5, 5)


# -----------------------------------------------------------------------------
# NIVEAU 2 — Sens inverse (exercice 2)
# -----------------------------------------------------------------------------

assert chaine_depuis_position(0, 0)   == 'A1'
assert chaine_depuis_position(1, 2)   == 'B3'
assert chaine_depuis_position(11, 11) == 'L12'


# -----------------------------------------------------------------------------
# NIVEAU 2 — Distance de Chebyshev (exercice 3)
# -----------------------------------------------------------------------------

assert distance_chebyshev(0, 0,  0,  0) == 0
assert distance_chebyshev(0, 0,  3,  3) == 3
assert distance_chebyshev(2, 2,  5,  4) == 3   # max(3, 2) = 3
assert distance_chebyshev(0, 0, 11, 11) == 11


# -----------------------------------------------------------------------------
# NIVEAU 3 — Aller-retour (exercice 4)
# -----------------------------------------------------------------------------

for case in ['A1', 'F6', 'L12', 'C8', 'H10']:
    col, lig = position_depuis_chaine(case)
    assert chaine_depuis_position(col, lig) == case, (
        f"Aller-retour échoué pour {case}"
    )

print("Tous les assert B1 passent ✓")
