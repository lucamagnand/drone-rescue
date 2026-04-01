# =============================================================================
# Corrigé — Module C1 : Configuration externe
# Fichier cible dans jeu/ : jeu/config.py + jeu/config.json
# =============================================================================

# NIVEAU 1 — Configuration minimale inline (sans fichier JSON externe)
# -----------------------------------------------------------------------------

CONFIG = {
    'grille_taille':           12,
    'nb_drones':               3,
    'nb_tempetes':             2,
    'nb_survivants':           5,
    'batterie_max':            10,
    'tours_max':               30,
    'cout_deplacement':        1,
    'cout_zone_x':             2,
    'cout_transport_survivant': 1,
    'recharge_stationnaire':   3,
    'proba_tempete_auto':      0.5,
    'intervalle_propagation_x': 5,
}

GRILLE_TAILLE             = CONFIG['grille_taille']
BATTERIE_MAX              = CONFIG['batterie_max']
TOURS_MAX                 = CONFIG['tours_max']
COUT_DEPLACEMENT          = CONFIG['cout_deplacement']
COUT_ZONE_X               = CONFIG['cout_zone_x']
COUT_TRANSPORT_SURVIVANT  = CONFIG['cout_transport_survivant']
RECHARGE_STATIONNAIRE     = CONFIG['recharge_stationnaire']

print(f"✅ Niveau 1 : GRILLE_TAILLE={GRILLE_TAILLE}, BATTERIE_MAX={BATTERIE_MAX}")


# NIVEAU 2 — Chargement robuste avec valeurs par défaut
# -----------------------------------------------------------------------------

def charger_config_robuste(config_dict, cle, valeur_defaut):
    """Retourne la valeur de la clé ou valeur_defaut si absente."""
    return config_dict.get(cle, valeur_defaut)


DEFAUTS = {
    'grille_taille': 12,
    'batterie_max': 10,
    'tours_max': 30,
    'cout_deplacement': 1,
    'cout_zone_x': 2,
    'cout_transport_survivant': 1,
    'recharge_stationnaire': 3,
    'proba_tempete_auto': 0.5,
    'intervalle_propagation_x': 5,
}

cfg_incomplet = {'grille_taille': 16}
for cle, defaut in DEFAUTS.items():
    valeur = charger_config_robuste(cfg_incomplet, cle, defaut)
    print(f'  {cle} = {valeur}')

print("✅ Niveau 2 : chargement robuste OK")


# NIVEAU 3 — Version complète intégrable dans jeu/config.py
# -----------------------------------------------------------------------------

import json
import os


def charger_config(chemin=None):
    """
    Charge le fichier config.json et retourne le dictionnaire de configuration.
    Utilise les valeurs par défaut si une clé est absente.

    Args:
        chemin (str|None): chemin vers config.json. Si None, utilise le dossier
                           du fichier courant.

    Returns:
        dict: configuration du jeu avec toutes les clés garanties.
    """
    if chemin is None:
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

    if not os.path.exists(chemin):
        print(f"[config] Fichier {chemin} introuvable. Valeurs par défaut utilisées.")
        return dict(DEFAUTS)

    with open(chemin, encoding='utf-8') as f:
        cfg = json.load(f)

    # Fusionner avec les défauts pour garantir toutes les clés
    config_complete = dict(DEFAUTS)
    config_complete.update(cfg)
    return config_complete


# Usage dans les autres modules :
#   from config import GRILLE_TAILLE, BATTERIE_MAX, COUT_ZONE_X
#
# On n'appelle charger_config() qu'une seule fois, au niveau module :
#   _cfg = charger_config()
#   GRILLE_TAILLE = _cfg['grille_taille']
#   ...

print("✅ Niveau 3 : charger_config() prête pour jeu/config.py")
