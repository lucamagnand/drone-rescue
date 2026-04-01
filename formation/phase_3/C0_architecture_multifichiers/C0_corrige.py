# =============================================================================
# Corrigé — Module C0 : Architecture multi-fichiers
# Fichier cible dans jeu/ : tous les fichiers (vue d'ensemble)
# =============================================================================
#
# NIVEAU 1 — Représentation minimale du graphe de dépendances
# -----------------------------------------------------------------------------

# Graphe de dépendances de Drone Rescue
GRAPHE_DEPENDANCES = {
    'main.py':      ['console.py', 'logger.py'],
    'console.py':   ['logique.py', 'affichage.py'],
    'logique.py':   ['config.py'],
    'affichage.py': ['config.py'],
    'config.py':    [],
    'logger.py':    [],
}

# Responsabilités
RESPONSABILITES = {
    'config.py':    'Lire config.json et exposer les constantes nommées',
    'logique.py':   'Toutes les règles métier du jeu',
    'affichage.py': 'Rendre la grille lisible en terminal',
    'console.py':   'Lire les saisies J1/J2 et orchestrer un tour',
    'logger.py':    'Écrire les événements dans un fichier de log',
    'main.py':      'Point d\'entrée, orchestration globale',
}


# =============================================================================
# NIVEAU 2 — Détection de violations
# -----------------------------------------------------------------------------

def est_import_valide(source: str, destination: str) -> bool:
    """
    Retourne True si `source` peut importer `destination` sans violer
    le graphe de dépendances acyclique de Drone Rescue.

    Règle : les dépendances vont toujours du niveau supérieur vers le niveau
    inférieur (main → console → logique/affichage → config).

    Args:
        source (str): fichier qui veut importer
        destination (str): fichier importé

    Returns:
        bool: True si l'import est valide
    """
    niveaux = {
        'config.py':    0,
        'logger.py':    1,
        'logique.py':   1,
        'affichage.py': 1,
        'console.py':   2,
        'main.py':      3,
    }
    niveau_src = niveaux.get(source, -1)
    niveau_dst = niveaux.get(destination, -1)
    return niveau_src > niveau_dst  # on importe toujours vers le bas


# Tests de validation
assert est_import_valide('logique.py',   'config.py')  is True
assert est_import_valide('logique.py',   'console.py') is False  # violation
assert est_import_valide('affichage.py', 'logique.py') is False  # violation
assert est_import_valide('console.py',   'logique.py') is True
assert est_import_valide('config.py',    'logique.py') is False  # violation
assert est_import_valide('main.py',      'console.py') is True
print("Tous les tests de validation réussis.")


# =============================================================================
# NIVEAU 3 — Affichage du graphe avec niveaux (version complète)
# -----------------------------------------------------------------------------

def afficher_graphe(graphe: dict) -> None:
    """
    Affiche le graphe de dépendances de manière lisible,
    trié par niveau de dépendance (du plus haut au plus bas).

    Args:
        graphe (dict): {fichier: [dépendances]}
    """
    niveaux = {
        'main.py':      3,
        'console.py':   2,
        'logique.py':   1,
        'affichage.py': 1,
        'logger.py':    1,
        'config.py':    0,
    }
    print("Graphe de dépendances — Drone Rescue")
    print("=" * 40)
    for fichier in sorted(graphe, key=lambda f: -niveaux.get(f, 0)):
        deps = graphe[fichier]
        if deps:
            print(f"  [N{niveaux.get(fichier,'?')}] {fichier:20s} → {', '.join(deps)}")
        else:
            print(f"  [N{niveaux.get(fichier,'?')}] {fichier:20s} → (aucune)")


if __name__ == '__main__':
    afficher_graphe(GRAPHE_DEPENDANCES)
