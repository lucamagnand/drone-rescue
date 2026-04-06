# =============================================================================
# Corrigé — Module C2 : Déboguer avec le logger
# Fichier cible dans jeu/ : jeu/logger.py
# =============================================================================

# NIVEAU 1 — Logger minimal en mémoire (compatible Colab)
# -----------------------------------------------------------------------------

_log = []

def ecrire_log(message):
    """Ajoute une ligne dans le log en mémoire."""
    _log.append(message)

def afficher_log():
    """Affiche toutes les lignes du log."""
    for ligne in _log:
        print(ligne)

def vider_log():
    """Vide le log."""
    _log.clear()


# État de test
etat = {
    'tour': 1, 'score': 0, 'partie_finie': False, 'victoire': False,
    'grille': [['.' for _ in range(12)] for _ in range(12)],
    'hopital': (0, 0), 'batiments': [],
    'drones': {
        'D1': {'id': 'D1', 'col': 2, 'lig': 3, 'batterie': 8, 'batterie_max': 10,
               'survivant': None, 'bloque': 0, 'hors_service': False},
    },
    'tempetes': {'T1': {'id': 'T1', 'col': 5, 'lig': 5, 'dx': 1, 'dy': 0}},
    'survivants': {'S1': {'id': 'S1', 'col': 3, 'lig': 3, 'etat': 'en_attente'}},
    'zones_x': set(), 'historique': [], 'nb_tours_max': 30,
}

print("✅ Niveau 1 : logger en mémoire prêt")


# NIVEAU 2 — Identifier et corriger les 3 bugs
# -----------------------------------------------------------------------------

# Bug 1 : col et lig inversés lors de la mise à jour de position
# Bug 2 : += au lieu de -= pour la consommation de batterie
# Bug 3 : condition de victoire toujours vraie (compare len avec len, pas nb_sauves)

def executer_mouvement_corrige(etat, id_drone, nouvelle_col, nouvelle_lig):
    """
    Version corrigée d'executer_mouvement.
    Cas nominal : déplacement simple sans zone X ni survivant.
    """
    drone = etat['drones'][id_drone]

    ecrire_log(f"[Tour {etat['tour']}] Avant : {id_drone} en ({drone['col']}, {drone['lig']})")

    # Correction Bug 1 : affecter correctement col et lig
    drone['col'] = nouvelle_col
    drone['lig'] = nouvelle_lig
    ecrire_log(f"[Tour {etat['tour']}] Après : {id_drone} en ({drone['col']}, {drone['lig']})")

    # Correction Bug 2 : consommer la batterie (soustraction)
    cout = 1
    drone['batterie'] -= cout
    ecrire_log(f"[Tour {etat['tour']}] Batterie après : {drone['batterie']}")

    # Correction Bug 3 : victoire seulement si TOUS les survivants sont sauvés
    nb_sauves = sum(1 for s in etat['survivants'].values() if s['etat'] == 'sauve')
    ecrire_log(f"[Tour {etat['tour']}] Survivants sauvés : {nb_sauves}/{len(etat['survivants'])}")
    if nb_sauves == len(etat['survivants']):
        etat['victoire'] = True
        etat['partie_finie'] = True

    return f"{id_drone} déplacé"


executer_mouvement_corrige(etat, 'D1', 4, 3)

assert etat['drones']['D1']['col'] == 4
assert etat['drones']['D1']['lig'] == 3
assert etat['drones']['D1']['batterie'] == 7
assert etat['partie_finie'] == False  # S1 n'est pas encore sauvé
print("✅ Niveau 2 : les 3 bugs corrigés")
print("Traces :")
afficher_log()


# NIVEAU 3 — Logger complet intégrable dans jeu/logger.py
# -----------------------------------------------------------------------------

import datetime
import os


class Logger:
    """
    Logger de partie pour Drone Rescue.
    Écrit dans un fichier texte daté, une ligne par action.
    """

    def __init__(self):
        """Initialise le logger sans fichier ouvert."""
        self._fichier = None

    def demarrer(self, dossier='.'):
        """Ouvre un nouveau fichier de log pour la partie."""
        nom = f"partie_{datetime.date.today()}.log"
        chemin = os.path.join(dossier, nom)
        self._fichier = open(chemin, 'a', encoding='utf-8')
        self.ecrire("=" * 40)
        self.ecrire(f"Nouvelle partie — {datetime.datetime.now().strftime('%H:%M:%S')}")

    def ecrire(self, message):
        """Ajoute une ligne dans le fichier de log."""
        if self._fichier:
            self._fichier.write(message + '\n')
            self._fichier.flush()  # écriture immédiate même si crash

    def fermer(self):
        """Ferme le fichier de log proprement."""
        if self._fichier:
            self.ecrire("Fin de partie.")
            self._fichier.close()
            self._fichier = None


# Usage (dans console.py) :
# from logger import Logger
# logger = Logger()
# logger.demarrer()
# logger.ecrire(f"[Tour {etat['tour']}] D1 déplacé vers C4")
# logger.fermer()

print("✅ Niveau 3 : classe Logger prête pour jeu/logger.py")
