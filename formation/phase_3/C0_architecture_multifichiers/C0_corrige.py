# =============================================================================
# Corrigé — Module C0 : Architecture multi-fichiers
# Fichier cible dans jeu/ : tous les fichiers (transversal)
# =============================================================================
#
# NIVEAU 1 — Solution minimale : fonctions de base pour analyser le graphe
# -----------------------------------------------------------------------------

# Graphe de dépendances réel du projet Drone Rescue
imports_projet = {
    'main.py':       ['logique', 'console', 'logger'],
    'console.py':    ['logique', 'affichage', 'config', 'logger'],
    'logique.py':    ['config'],
    'affichage.py':  ['config'],
    'logger.py':     [],
    'config.py':     [],
}


def importeurs(fichier, graphe):
    """Retourne la liste des fichiers qui importent 'fichier'."""
    nom = fichier.replace('.py', '')
    return [source for source, cibles in graphe.items() if nom in cibles]


def fichiers_feuilles(graphe):
    """Retourne les fichiers sans dépendance vers le projet (briques de base)."""
    return [f for f, deps in graphe.items() if len(deps) == 0]


def import_circulaire(a, b, graphe):
    """Retourne True si a importe b ET b importe a (cycle direct)."""
    nom_a = a.replace('.py', '')
    nom_b = b.replace('.py', '')
    a_importe_b = nom_b in graphe.get(a, [])
    b_importe_a = nom_a in graphe.get(b, [])
    return a_importe_b and b_importe_a


# --- Vérifications niveau 1 ---
assert 'main.py' in importeurs('logique', imports_projet)
assert importeurs('main.py', imports_projet) == []
assert 'config.py' in fichiers_feuilles(imports_projet)
assert import_circulaire('logique.py', 'console.py', imports_projet) == False
print("Niveau 1 : OK")


# NIVEAU 2 — Enrichissement : détection de cycle indirect (chemin quelconque)
# -----------------------------------------------------------------------------

def chemin_existe(source, cible, graphe, vus=None):
    """Retourne True si source peut atteindre cible (directement ou indirectement)."""
    if vus is None:
        vus = set()
    if source in vus:
        return False
    vus.add(source)
    nom_source = source.replace('.py', '')
    # Chercher les voisins directs (fichiers importés par source)
    for dep in graphe.get(source, []):
        dep_py = dep + '.py' if not dep.endswith('.py') else dep
        if dep == cible or dep_py == cible:
            return True
        if chemin_existe(dep_py, cible, graphe, vus):
            return True
    return False


def cycle_indirect(a, b, graphe):
    """Retourne True si a peut atteindre b ET b peut atteindre a."""
    return chemin_existe(a, b, graphe) and chemin_existe(b, a, graphe)


# Graphe sain : pas de cycle même indirect
assert not cycle_indirect('logique.py', 'config.py', imports_projet)
print("Niveau 2 : OK")


# NIVEAU 3 — Version complète : rapport complet du graphe
# (identique à ce qu'on produirait dans un vrai outil d'analyse)
# -----------------------------------------------------------------------------

def rapport_graphe(graphe):
    """Affiche un rapport complet du graphe de dépendances."""
    print("=" * 60)
    print("RAPPORT DU GRAPHE DE DÉPENDANCES")
    print("=" * 60)

    print("\n📌 Fichiers feuilles (aucune dépendance interne) :")
    for f in fichiers_feuilles(graphe):
        print(f"   {f}")

    print("\n📌 Fichiers racines (personne ne les importe) :")
    for f in graphe:
        if importeurs(f, graphe) == []:
            print(f"   {f}")

    print("\n📌 Dépendances détaillées :")
    for fichier, deps in graphe.items():
        if deps:
            print(f"   {fichier} importe : {', '.join(deps)}")
        else:
            print(f"   {fichier} : aucune dépendance interne")

    print("\n📌 Vérification des cycles directs :")
    fichiers = list(graphe.keys())
    cycle_detecte = False
    for i in range(len(fichiers)):
        for j in range(i + 1, len(fichiers)):
            if import_circulaire(fichiers[i], fichiers[j], graphe):
                print(f"   ⚠️  CYCLE : {fichiers[i]} ↔ {fichiers[j]}")
                cycle_detecte = True
    if not cycle_detecte:
        print("   ✅ Aucun cycle direct détecté")

    print("=" * 60)


rapport_graphe(imports_projet)
