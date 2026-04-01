# =============================================================================
# Corrigé — Module A2 : Choisir ses structures de données
# Fichier cible dans jeu/ : jeu/logique.py — initialisation de etat
# =============================================================================
#
# NIVEAU 1 — Solution minimale (le strict nécessaire pour que ça fonctionne)
# -----------------------------------------------------------------------------

def creer_etat_vide_v1():
    """Retourne un état global vide — version minimale."""
    return {
        "tour": 0,
        "score": 0,
        "partie_finie": False,
        "victoire": False,
        "grille": [[" . "] * 12 for _ in range(12)],  # list[list[str]]
        "hopital": (0, 0),                             # tuple(col, lig)
        "batiments": [],                               # list[tuple]
        "drones": {},                                  # dict
        "tempetes": {},                                # dict
        "survivants": {},                              # dict
        "zones_x": set(),                             # set
        "historique": [],                              # list
    }


# Démonstration des opérations de base
etat = creer_etat_vide_v1()

# Accès dict : O(1)
etat["drones"]["D1"] = {"id": "D1", "col": 0, "lig": 0, "batterie": 20}
batterie = etat["drones"]["D1"]["batterie"]

# Appartenance set : O(1)
etat["zones_x"].add((3, 5))
print("(3, 5) est dangereuse ?", (3, 5) in etat["zones_x"])  # True

# Ajout list : O(1) amorti
etat["historique"].append("tour 1 : D1 se déplace en A1")

print("État minimal créé ✅")


# NIVEAU 2 — Enrichissement (robustesse, cas limites)
# -----------------------------------------------------------------------------

COL_LETTRES = list("ABCDEFGHIJKL")  # 12 colonnes : A à L


def verifier_structures(etat):
    """Vérifie que les structures de etat sont du bon type.

    Retourne (True, '') si tout est correct,
    ou (False, message_erreur) sinon.
    """
    attendu = {
        "tour": int,
        "score": int,
        "partie_finie": bool,
        "victoire": bool,
        "grille": list,
        "hopital": tuple,
        "batiments": list,
        "drones": dict,
        "tempetes": dict,
        "survivants": dict,
        "zones_x": set,
        "historique": list,
    }
    for cle, type_attendu in attendu.items():
        if cle not in etat:
            return False, f"Clé manquante : '{cle}'"
        if not isinstance(etat[cle], type_attendu):
            return False, (
                f"'{cle}' : attendu {type_attendu.__name__}, "
                f"reçu {type(etat[cle]).__name__}"
            )
    # Vérifier la grille : 12 lignes de 12 colonnes
    if len(etat["grille"]) != 12:
        return False, "grille doit avoir 12 lignes"
    for i, ligne in enumerate(etat["grille"]):
        if not isinstance(ligne, list) or len(ligne) != 12:
            return False, f"grille[{i}] doit être une liste de 12 éléments"
    return True, ""


etat2 = creer_etat_vide_v1()
ok, msg = verifier_structures(etat2)
print(f"Structures valides : {ok} {msg}")


# NIVEAU 3 — Version complète intégrable dans jeu/ (proche du code réel)
# -----------------------------------------------------------------------------

def creer_etat_initial(config):
    """Crée l'état global initial à partir de la configuration.

    Args:
        config (dict): dictionnaire de configuration issu de config.json.
            Clés attendues : GRILLE_TAILLE, HOPITAL_COL, HOPITAL_LIG,
            NB_BATIMENTS, BATIMENTS_POSITIONS.

    Returns:
        dict: état global initialisé avec les bonnes structures.
    """
    taille = config.get("GRILLE_TAILLE", 12)

    etat = {
        "tour": 0,
        "score": 0,
        "partie_finie": False,
        "victoire": False,
        # list[list[str]] — grille vide de taille × taille
        "grille": [[" . "] * taille for _ in range(taille)],
        # tuple immuable et hashable → peut être clé de dict ou élément de set
        "hopital": (config.get("HOPITAL_COL", 0), config.get("HOPITAL_LIG", 0)),
        # list[tuple] — positions fixes des bâtiments
        "batiments": [
            tuple(pos)
            for pos in config.get("BATIMENTS_POSITIONS", [])
        ],
        # dict — accès O(1) par identifiant ex: etat["drones"]["D1"]
        "drones": {},
        # dict — accès O(1) par identifiant ex: etat["tempetes"]["T1"]
        "tempetes": {},
        # dict — accès O(1) par identifiant ex: etat["survivants"]["S1"]
        "survivants": {},
        # set de tuples — appartenance O(1) : (col, lig) in etat["zones_x"]
        "zones_x": set(),
        # list — journal chronologique (ordre important, doublons possibles)
        "historique": [],
    }

    # Placer le symbole hôpital dans la grille
    col_h, lig_h = etat["hopital"]
    etat["grille"][lig_h][col_h] = " H "

    # Placer les bâtiments dans la grille
    for col_b, lig_b in etat["batiments"]:
        etat["grille"][lig_b][col_b] = " B "

    return etat


# Test avec une config minimale
config_test = {
    "GRILLE_TAILLE": 12,
    "HOPITAL_COL": 0,
    "HOPITAL_LIG": 0,
    "BATIMENTS_POSITIONS": [[2, 3], [5, 7]],
}
etat3 = creer_etat_initial(config_test)
ok3, msg3 = verifier_structures(etat3)
print(f"\nÉtat initial complet — structures valides : {ok3} {msg3}")
print(f"Hôpital en grille[0][0] : {etat3['grille'][0][0]}")
print(f"Bâtiment en grille[3][2] : {etat3['grille'][3][2]}")
print(f"Zones X (vide) : {etat3['zones_x']}")
