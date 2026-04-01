# =============================================================================
# Corrigé — Module A3 : Pseudo-code d'un tour de jeu complet
# Fichier cible dans jeu/ : jeu/console.py — boucle_de_jeu(), phase_j1(),
#                           phase_j2(), fin_de_tour()
# =============================================================================
#
# NIVEAU 1 — Solution minimale (squelette avec pseudo-code en commentaires)
# -----------------------------------------------------------------------------

def boucle_de_jeu_v1(etat):
    """Boucle principale du jeu — version squelette.

    Chaque étape du pseudo-code est traduite en appel de fonction.
    Les fonctions elles-mêmes sont implémentées dans les modules suivants.
    """
    while not etat["partie_finie"]:
        # Étape 1 : afficher la grille et le score courant
        afficher_grille(etat)
        afficher_score(etat)

        # Étape 2 : phase J1 — jusqu'à MAX_DEPLACEMENTS mouvements de drones
        phase_j1(etat)

        # Étape 3 : phase J2 — jusqu'à MAX_DEPLACEMENTS_J2 mouvements de tempêtes
        phase_j2(etat)

        # Étape 4 : météo automatique — chaque tempête a 50% de se déplacer
        deplacer_tempetes(etat)

        # Étape 5 : propagation des zones de danger
        propager_zones_x(etat)

        # Étape 6 : vérifier si la partie est terminée (victoire ou défaite)
        verifier_fin_partie(etat)

        # Étape 7 : enregistrer les actions dans l'historique
        enregistrer_historique(etat)

        # Étape 8 : incrémenter le compteur de tours
        etat["tour"] += 1


# NIVEAU 2 — Enrichissement : squelette de phase_j1 et phase_j2
# -----------------------------------------------------------------------------

MAX_DEPLACEMENTS_J1 = 3
MAX_DEPLACEMENTS_J2 = 2


def phase_j1_v2(etat):
    """Phase J1 : le joueur 1 effectue jusqu'à MAX_DEPLACEMENTS mouvements.

    Chaque mouvement suit le cycle : lire → valider → exécuter.
    J1 peut s'arrêter avant MAX_DEPLACEMENTS en tapant 'stop'.
    """
    nb_deplacements = 0

    while nb_deplacements < MAX_DEPLACEMENTS_J1:
        # a. Lire la saisie de J1 : identifiant drone + destination
        saisie = input(f"J1 (dépl. {nb_deplacements + 1}/{MAX_DEPLACEMENTS_J1}) > ").strip()

        # b. Permettre à J1 de passer le reste de ses déplacements
        if saisie.lower() == "stop":
            break

        # c. Parser la saisie (ex : "D1 B4" → drone_id="D1", destination=(1, 3))
        ok_parse, drone_id, destination = parser_saisie_j1(saisie)
        if not ok_parse:
            print("Format invalide. Exemple : D1 B4")
            continue  # ne pas décrémenter le compteur

        # d. Valider le mouvement (pure, sans effet de bord)
        valide, message = valider_mouvement(etat, drone_id, destination)
        if not valide:
            print(f"Mouvement invalide : {message}")
            continue  # ne pas décrémenter le compteur

        # e. Exécuter le mouvement (modifie etat)
        log = executer_mouvement(etat, drone_id, destination)
        etat["historique"].append(log)
        nb_deplacements += 1


def phase_j2_v2(etat):
    """Phase J2 : le joueur 2 effectue jusqu'à MAX_DEPLACEMENTS_J2 mouvements.

    Même structure que phase_j1 mais pour les tempêtes.
    """
    nb_deplacements = 0

    while nb_deplacements < MAX_DEPLACEMENTS_J2:
        saisie = input(f"J2 (dépl. {nb_deplacements + 1}/{MAX_DEPLACEMENTS_J2}) > ").strip()

        if saisie.lower() == "stop":
            break

        ok_parse, tempete_id, destination = parser_saisie_j2(saisie)
        if not ok_parse:
            print("Format invalide. Exemple : T1 C5")
            continue

        valide, message = valider_mouvement_tempete(etat, tempete_id, destination)
        if not valide:
            print(f"Mouvement invalide : {message}")
            continue

        log = executer_mouvement_tempete(etat, tempete_id, destination)
        etat["historique"].append(log)
        nb_deplacements += 1


# NIVEAU 3 — Version complète intégrable dans jeu/ (proche du code réel)
# -----------------------------------------------------------------------------

def boucle_de_jeu_v3(etat):
    """Boucle principale complète avec gestion de la fin de partie.

    Affiche le résultat final après la dernière itération.
    """
    while not etat["partie_finie"]:
        afficher_grille(etat)
        afficher_score(etat)
        phase_j1(etat)
        phase_j2(etat)
        deplacer_tempetes(etat)
        propager_zones_x(etat)
        verifier_fin_partie(etat)
        enregistrer_historique(etat)
        etat["tour"] += 1

    # Après la boucle : affichage du résultat final
    afficher_grille(etat)
    if etat.get("victoire"):
        print(f"Victoire ! Tous les survivants ont été sauvés en {etat['tour']} tours.")
        print(f"Score final : {etat['score']}")
    else:
        print(f"Défaite. La partie s'est arrêtée au tour {etat['tour']}.")
        print(f"Score final : {etat['score']}")


# --- Stubs pour permettre l'exécution de ce corrigé sans les vrais modules ---

def afficher_grille(etat):
    print(f"[grille] tour {etat['tour']}")

def afficher_score(etat):
    print(f"[score] {etat['score']}")

def phase_j1(etat):
    pass

def phase_j2(etat):
    pass

def deplacer_tempetes(etat):
    pass

def propager_zones_x(etat):
    pass

def verifier_fin_partie(etat):
    if etat["tour"] >= 2:
        etat["partie_finie"] = True
        etat["victoire"] = True

def enregistrer_historique(etat):
    etat["historique"].append(f"tour {etat['tour']} enregistré")

def parser_saisie_j1(saisie):
    return True, "D1", (0, 1)

def parser_saisie_j2(saisie):
    return True, "T1", (2, 3)

def valider_mouvement(etat, drone_id, destination):
    return True, ""

def valider_mouvement_tempete(etat, tempete_id, destination):
    return True, ""

def executer_mouvement(etat, drone_id, destination):
    return f"D1 → {destination}"

def executer_mouvement_tempete(etat, tempete_id, destination):
    return f"T1 → {destination}"


# Test rapide
if __name__ == "__main__":
    etat_test = {
        "tour": 0,
        "score": 0,
        "partie_finie": False,
        "victoire": False,
        "historique": [],
    }
    boucle_de_jeu_v3(etat_test)
    print(f"\nHistorique : {etat_test['historique']}")
