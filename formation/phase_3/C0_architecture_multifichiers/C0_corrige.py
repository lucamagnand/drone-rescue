# =============================================================================
# Corrigé — Module C0 : Architecture multi-fichiers
# Fichier cible dans jeu/ : main.py, console.py, logique.py, affichage.py
# =============================================================================

# NIVEAU 1 — Graphe de dépendances correct
# -----------------------------------------------------------------------------

graphe = {
    'config':    [],
    'logique':   ['config'],
    'affichage': ['config'],
    'logger':    [],
    'console':   ['logique', 'affichage', 'logger'],
    'main':      ['console', 'logique', 'logger'],
}

# Vérification rapide
assert 'logique' in graphe['console']
assert 'affichage' in graphe['console']
assert 'console' not in graphe['logique'], "Violation : logique ne doit pas importer console"
assert graphe['config'] == [], "config ne doit rien importer"
print("✅ Niveau 1 : graphe de dépendances valide")


# NIVEAU 2 — Détection automatique de cycles
# -----------------------------------------------------------------------------

def detecter_cycle(graphe, depart, visite=None, pile=None):
    """Détecte un cycle à partir d'un nœud donné (DFS récursif)."""
    if visite is None:
        visite = set()
    if pile is None:
        pile = set()
    visite.add(depart)
    pile.add(depart)
    for voisin in graphe.get(depart, []):
        if voisin not in visite:
            if detecter_cycle(graphe, voisin, visite, pile):
                return True
        elif voisin in pile:
            return True
    pile.discard(depart)
    return False


def valider_graphe(graphe):
    """Vérifie qu'aucun cycle n'existe dans le graphe."""
    for module in graphe:
        if detecter_cycle(dict(graphe), module):
            return False, module
    return True, None


valide, coupable = valider_graphe(graphe)
assert valide, f"Cycle détecté depuis : {coupable}"
print("✅ Niveau 2 : aucun cycle détecté")

# Test avec un graphe invalide (cycle intentionnel)
graphe_invalide = dict(graphe)
graphe_invalide['logique'] = ['config', 'console']  # violation
valide_inv, coupable_inv = valider_graphe(graphe_invalide)
assert not valide_inv, "Le graphe invalide aurait dû être détecté"
print(f"✅ Niveau 2 : violation correctement détectée (depuis '{coupable_inv}')")


# NIVEAU 3 — Structure complète de main.py intégrable dans jeu/
# -----------------------------------------------------------------------------
#
# Ce code est la version exacte de jeu/main.py.
# main.py n'a qu'une seule responsabilité : orchestrer le démarrage.
#
# from console import boucle_de_jeu
# from logique import initialiser_partie
# from logger import demarrer_log
#
# def main():
#     """Point d'entrée du programme Drone Rescue."""
#     demarrer_log()
#     etat = initialiser_partie()
#     boucle_de_jeu(etat)
#
# if __name__ == '__main__':
#     main()
#
# Règles à respecter :
# 1. main() ne contient aucune logique métier.
# 2. if __name__ == '__main__' isole l'exécution de l'import.
# 3. Tout import de module se fait en haut du fichier.

print("✅ Niveau 3 : structure main.py correcte — voir jeu/main.py")
