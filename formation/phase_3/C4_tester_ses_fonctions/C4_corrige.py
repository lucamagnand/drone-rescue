# =============================================================================
# C4_corrige.py — Tester ses fonctions
# Fichier cible dans jeu/ : jeu/logique.py + tests/test_logique.py
# =============================================================================
#
# NIVEAU 1 — Solution minimale : 5 tests avec assert
# -----------------------------------------------------------------------------

# Constantes (reproduites depuis config.json)
GRILLE_TAILLE = 12
BATTERIE_INIT = 15
COUT_ZONE_X = 2
COUT_TRANSPORT = 2


# Fonctions simulées (version pédagogique — pas de dépendance vers jeu/)
def creer_drone(drone_id: str, col: int, lig: int,
                batterie_max: int = BATTERIE_INIT) -> dict:
    """Retourne un dictionnaire représentant un drone neuf."""
    return {
        "id": drone_id,
        "col": col,
        "lig": lig,
        "batterie": batterie_max,
        "batterie_max": batterie_max,
        "survivant": None,
        "bloque": 0,
        "hors_service": False,
    }


def valider_mouvement(etat: dict, drone: dict, cible: tuple) -> tuple:
    """Retourne (bool, str) : mouvement autorisé ou refusé avec raison."""
    col_c, lig_c = cible
    if drone["hors_service"]:
        return False, "drone hors service"
    if drone["bloque"] > 0:
        return False, "drone bloqué"
    if not (0 <= col_c < GRILLE_TAILLE and 0 <= lig_c < GRILLE_TAILLE):
        return False, "cible hors grille"
    if max(abs(col_c - drone["col"]), abs(lig_c - drone["lig"])) > 1:
        return False, "déplacement trop grand (distance Chebyshev > 1)"
    if cible in etat.get("batiments", []):
        return False, "case bâtiment"
    cout = COUT_TRANSPORT if drone.get("survivant") else 1
    if cible in etat.get("zones_x", set()):
        cout += COUT_ZONE_X
    if drone["batterie"] < cout:
        return False, f"batterie insuffisante (coût={cout}, batterie={drone['batterie']})"
    return True, "ok"


def etat_minimal(batiments=None, zones_x=None) -> dict:
    """Construit un état de jeu minimal pour les tests."""
    return {
        "batiments": batiments or [],
        "zones_x": zones_x or set(),
        "hopital": (0, 0),
    }


# ---------------------------------------------------------------------------
# Tests niveau 1 — 5 cas avec assert
# ---------------------------------------------------------------------------

def test_creer_drone_structure():
    """creer_drone retourne un dict avec toutes les clés attendues."""
    drone = creer_drone("D1", col=5, lig=3)
    assert drone["id"] == "D1"
    assert drone["col"] == 5
    assert drone["lig"] == 3
    assert drone["batterie"] == BATTERIE_INIT
    assert drone["batterie_max"] == BATTERIE_INIT
    assert drone["survivant"] is None
    assert drone["bloque"] == 0
    assert drone["hors_service"] is False
    print("  ✓ test_creer_drone_structure")


def test_valider_mouvement_cas_valide():
    """Un déplacement d'une case est accepté."""
    etat = etat_minimal()
    drone = creer_drone("D1", col=3, lig=3)
    ok, raison = valider_mouvement(etat, drone, cible=(4, 3))
    assert ok, f"Attendu True, got False : {raison}"
    print("  ✓ test_valider_mouvement_cas_valide")


def test_valider_mouvement_hors_service():
    """Un drone hors_service=True ne peut pas se déplacer."""
    etat = etat_minimal()
    drone = creer_drone("D1", col=3, lig=3)
    drone["hors_service"] = True
    ok, raison = valider_mouvement(etat, drone, cible=(4, 3))
    assert not ok
    assert "hors service" in raison
    print("  ✓ test_valider_mouvement_hors_service")


def test_valider_mouvement_trop_loin():
    """Un déplacement de 2 cases est refusé."""
    etat = etat_minimal()
    drone = creer_drone("D1", col=0, lig=0)
    ok, raison = valider_mouvement(etat, drone, cible=(2, 0))
    assert not ok
    print("  ✓ test_valider_mouvement_trop_loin")


def test_valider_mouvement_batterie_insuffisante_zone_x():
    """Batterie 1 insuffisante pour zone X (coût = 1 + 2 = 3)."""
    cible = (4, 3)
    etat = etat_minimal(zones_x={cible})
    drone = creer_drone("D1", col=3, lig=3)
    drone["batterie"] = 1
    ok, raison = valider_mouvement(etat, drone, cible)
    assert not ok
    assert "insuffisant" in raison.lower(), f"Message inattendu : {raison}"
    print("  ✓ test_valider_mouvement_batterie_insuffisante_zone_x")


# NIVEAU 2 — Enrichissement : cas limites supplémentaires
# -----------------------------------------------------------------------------

def test_valider_mouvement_bloque():
    """Un drone bloqué (bloque=1) ne peut pas se déplacer."""
    etat = etat_minimal()
    drone = creer_drone("D1", col=3, lig=3)
    drone["bloque"] = 1
    ok, raison = valider_mouvement(etat, drone, cible=(4, 3))
    assert not ok
    assert "bloqué" in raison
    print("  ✓ test_valider_mouvement_bloque")


def test_valider_mouvement_batiment():
    """Un drone ne peut pas entrer sur un bâtiment."""
    cible = (4, 3)
    etat = etat_minimal(batiments=[cible])
    drone = creer_drone("D1", col=3, lig=3)
    ok, raison = valider_mouvement(etat, drone, cible)
    assert not ok
    assert "bâtiment" in raison
    print("  ✓ test_valider_mouvement_batiment")


def test_valider_mouvement_hors_grille():
    """Un drone ne peut pas sortir de la grille."""
    etat = etat_minimal()
    drone = creer_drone("D1", col=0, lig=0)
    ok, raison = valider_mouvement(etat, drone, cible=(-1, 0))
    assert not ok
    assert "grille" in raison
    print("  ✓ test_valider_mouvement_hors_grille")


def test_valider_mouvement_batterie_juste_suffisante():
    """Batterie exactement égale au coût : mouvement accepté."""
    cible = (4, 3)
    etat = etat_minimal(zones_x={cible})
    drone = creer_drone("D1", col=3, lig=3)
    drone["batterie"] = 3  # coût exact = 1 + 2
    ok, raison = valider_mouvement(etat, drone, cible)
    assert ok, f"Batterie 3 = coût 3, devrait être accepté : {raison}"
    print("  ✓ test_valider_mouvement_batterie_juste_suffisante")


# NIVEAU 3 — Exécuteur de tests autonome (sans pytest)
# -----------------------------------------------------------------------------


def executer_tous_les_tests():
    """
    Lance tous les tests et affiche le bilan.
    Compatible avec `python C4_corrige.py` sans pytest.
    """
    tests = [
        # Niveau 1
        test_creer_drone_structure,
        test_valider_mouvement_cas_valide,
        test_valider_mouvement_hors_service,
        test_valider_mouvement_trop_loin,
        test_valider_mouvement_batterie_insuffisante_zone_x,
        # Niveau 2
        test_valider_mouvement_bloque,
        test_valider_mouvement_batiment,
        test_valider_mouvement_hors_grille,
        test_valider_mouvement_batterie_juste_suffisante,
    ]

    print(f"=== C4 — Lancement de {len(tests)} tests ===")
    echecs = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"  ✗ {t.__name__} — AssertionError : {e}")
            echecs += 1
        except Exception as e:
            print(f"  ✗ {t.__name__} — Erreur inattendue : {e}")
            echecs += 1

    print()
    if echecs == 0:
        print(f"TOUS LES TESTS PASSENT ({len(tests)} tests)")
    else:
        print(f"{echecs} ÉCHEC(S) sur {len(tests)} tests")
    print()
    print("Pour aller plus loin : pytest tests/test_logique.py -v")


if __name__ == "__main__":
    executer_tous_les_tests()
