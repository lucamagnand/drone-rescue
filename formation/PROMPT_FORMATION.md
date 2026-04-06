# Prompt de génération — Modules de formation Drone Rescue

> **Usage** : ce fichier est un prompt autonome destiné à être soumis à un LLM
> (ChatGPT, Claude, Perplexity, Gemini…) **sans contexte préalable**.
> Il contient tout ce qu'une IA doit savoir pour produire les modules de
> formation sans ambiguïté.

---

## Contexte du projet

Le dépôt GitHub `lucamagnand/drone-rescue` contient un jeu Python pédagogique
destinés à des étudiants **débutants en programmation** (1ère année d'école
d'ingénieurs). Le jeu simule une mission de sauvetage par drones sur une grille
12×12. Deux joueurs s'affrontent : J1 pilote les drones de secours, J2 déplace
les tempêtes pour les en empêcher.

### Architecture existante du repo

```
drone-rescue/
├── jeu/                        ← CODE SOURCE DU JEU (cible finale des étudiants)
│   ├── main.py                 ← point d'entrée : initialise et lance la partie
│   ├── logique.py              ← toutes les règles métier (≈ 600 lignes)
│   ├── console.py              ← boucle de jeu, saisie J1 et J2, affichage
│   ├── affichage.py            ← rendu de la grille en terminal
│   ├── config.py               ← lecture de config.json, expose les constantes
│   ├── config.json             ← source de vérité de toutes les constantes
│   └── logger.py               ← écriture des logs de partie
├── cours/                      ← 10 modules de cours Markdown existants (00→09)
│   ├── 00_introduction.md
│   ├── 01_structures_de_base.md
│   ├── 02_boucles_et_conditions.md
│   ├── 03_fonctions.md
│   ├── 04_modules_et_io.md
│   ├── 05_dictionnaires_avances.md
│   ├── 06_grille_et_affichage.md
│   ├── 07_logique_de_jeu.md
│   ├── 08_console_et_log.md
│   ├── 09_assemblage_final.md
│   └── annexe_formatage.md
├── exercices/                  ← 9 exercices .py existants (ex_01 → ex_09)
├── corrections/                ← corrigés des exercices existants
├── notebooks/                  ← notebooks Jupyter existants
├── tests/                      ← tests unitaires existants
├── REFERENTIEL_ENSEIGNEMENTS.md← référentiel complet des notions Python du jeu
├── GUIDE_FORMATEUR.md          ← guide pédagogique pour l'enseignant
└── GIT_BASH_GUIDE.md           ← guide Git pour les étudiants
```

### Contraintes pédagogiques connues

- **Aucune classe Python (POO)** : toutes les entités sont des dictionnaires.
  Ce choix est intentionnel et documenté dans `REFERENTIEL_ENSEIGNEMENTS.md`.
- **Tout est en français** : code, commentaires, docstrings, cours.
- **Public cible** : étudiants n'ayant jamais programmé, en 1ère année.
- **Environnement** : Python 3.10+, terminal, compatible Google Colab.
- **Pas de bibliothèques externes** : uniquement `random`, `json`, `os`,
  `datetime` de la stdlib Python.

### Structures de données clés du jeu

Toutes les entités sont des dictionnaires Python :

```python
# Drone
{ "id": str, "col": int, "lig": int,
  "batterie": int, "batterie_max": int,
  "survivant": str|None, "bloque": int, "hors_service": bool }

# Tempête
{ "id": str, "col": int, "lig": int, "dx": int, "dy": int }

# Survivant
{ "id": str, "col": int, "lig": int,
  "etat": "en_attente"|"embarque"|"sauve" }

# État global de la partie
etat = {
    "tour": int, "score": int,
    "partie_finie": bool, "victoire": bool,
    "grille": list[list[str]],   # grille[lig][col], 12×12
    "hopital": (col, lig),
    "batiments": [(col, lig), ...],
    "drones": { "D1": {drone_dict}, ... },
    "tempetes": { "T1": {tempete_dict}, ... },
    "survivants": { "S1": {survivant_dict}, ... },
    "zones_x": {(col, lig), ...},   # set de tuples
    "historique": [str, ...],
}
```

### Règles du jeu (résumé)

- Grille 12×12, repérée par lettres (A–L) en colonne et numéros (1–12) en ligne
- Symboles grille : `H` hôpital, `B` bâtiment, `D` drone, `T` tempête,
  `S` survivant en attente, `X` zone de danger, `.` case vide
- **J1** déplace ses drones (max 1 case, distance Chebyshev), max 3 déplacements/tour
- **J2** déplace ses tempêtes (max 1 case), max 2 déplacements/tour
- Coût batterie : 1 par déplacement, +1 si transport survivant, +2 si zone X
- Recharge : +3 batterie si drone stationnaire ou arrivant à l'hôpital
- Collision drone+tempête : drone bloqué 2 tours
- Batterie à 0 en vol : drone hors service définitivement
- Fin de partie : tous survivants sauvés (victoire) OU tours max dépassés
  OU tous drones hors service (défaite)
- Phase météo automatique en fin de tour : chaque tempête a 50% de se déplacer
- Zones X se propagent tous les N tours (probabilité configurable)

---

## Objectif de la tâche

Créer un dossier `formation/` complet dans le repo, sur la branche
`feature/formation`, contenant une **série de modules de formation guidés**
permettant à un étudiant débutant de passer **de la feuille blanche au code
complet de `jeu/`**, étape par étape.

Le dossier `formation/` **ne remplace pas** `cours/` et `exercices/` existants.
Il les **complète** avec les couches manquantes : conception, algorithmique,
architecture, et transversal.

---

## Structure à produire

```
formation/
├── README.md                        ← vue d'ensemble du parcours complet
├── phase_0/                         ← Comprendre avant de coder
│   ├── A0_regles_et_representation/
│   │   ├── A0.md
│   │   ├── A0.ipynb
│   │   └── A0_corrige.py
│   ├── A1_entites_et_attributs/
│   │   ├── A1.md
│   │   ├── A1.ipynb
│   │   └── A1_corrige.py
│   ├── A2_choix_structures_donnees/
│   │   ├── A2.md
│   │   ├── A2.ipynb
│   │   └── A2_corrige.py
│   └── A3_pseudocode_tour_de_jeu/
│       ├── A3.md
│       ├── A3.ipynb
│       └── A3_corrige.py
├── phase_1/                         ← Liant algorithmique
│   └── B0_tracer_a_la_main/
│       ├── B0.md
│       ├── B0.ipynb
│       └── B0_corrige.py
├── phase_2/                         ← Construire couche par couche
│   ├── P01_config/
│   ├── P02_entites/
│   ├── P03_affichage/
│   ├── P04_validation/
│   ├── P05_execution_nominal/
│   ├── P06_cas_limites/
│   ├── P07_console_j1/
│   ├── P08_console_j2/
│   └── P09_assemblage/
└── phase_3/                         ← Savoirs transversaux
    ├── C0_architecture_multifichiers/
    ├── C1_configuration_externe/
    ├── C2_deboguer_avec_logger/
    ├── C3_versionner_git/
    └── C4_tester_ses_fonctions/
```

Chaque dossier de module contient **3 fichiers** :

### Fichier 1 : `XN.md` — Théorie et principes

Structure obligatoire de chaque `.md` :

```markdown
# Module XN — [Titre]

## Positionnement dans le parcours
- **Phase** : [Phase 0/1/2/3]
- **Prérequis** : [liste des modules XN précédents requis]
- **Requis par** : [liste des modules XN qui dépendent de celui-ci]
- **Fichier(s) cible(s) dans jeu/** : [ex: `jeu/logique.py` — fonctions `creer_drone()`, `creer_survivant()`]
- **Durée estimée** : [ex: 45 min]

## Objectif
[Ce que l'étudiant sait faire à la fin de ce module, formulé en verbe d'action]

## Le QUOI — Définition et concept
[Explication claire du concept, avec exemple concret tiré du jeu]

## Le POURQUOI — Enjeu pédagogique
[Pourquoi ce concept est indispensable pour construire le jeu]

## Les RISQUES
### Si on ne le fait pas
[Conséquence concrète sur le jeu ou le code]
### Si on le fait mal
[Bug ou comportement inattendu typique, avec exemple]

## Lien avec jeu/
[Extrait de code réel du fichier cible, commenté, avec numéros de lignes]

## Prompts LLM pour aller plus loin
[3 à 5 prompts génériques, formulés en français, que l'étudiant peut
copier-coller dans n'importe quel LLM pour approfondir, débloquer
ou étendre ses connaissances. Chaque prompt est autonome et précis.]

Exemple de format :
> **Prompt 1 — Approfondir**
> « Explique-moi la différence entre un dictionnaire et une liste en Python,
>   avec des exemples tirés d'un jeu de plateau. »

> **Prompt 2 — Débloquer**
> « En Python, j'ai un dictionnaire `drone` avec une clé `batterie`.
>   Comment modifier sa valeur sans créer un nouveau dictionnaire ? »
```

### Fichier 2 : `XN.ipynb` — Notebook Jupyter

Structure obligatoire de chaque notebook :

```
Section 1 — Rappels synthétiques (cellules Markdown)
  - Résumé des notions du module courant (tableau ou liste concise)
  - Rappel des prérequis du module précédent (ce qu'on a vu juste avant)
  - Compatible Google Colab : pas d'import de fichiers locaux
    (reproduire inline les données nécessaires)

Section 2 — Exercice guidé pas-à-pas (cellules alternées Markdown + Code)
  - Chaque cellule de code a un objectif affiché clairement
  - Progression du simple au complexe
  - Cellules avec `# TODO :` indiquant ce que l'étudiant doit compléter
  - Cellules de vérification (`assert` ou `print`) après chaque étape
  - Jamais de corrigé inline : renvoyer vers XN_corrige.py
```

### Fichier 3 : `XN_corrige.py` — Corrigé progressif

Structure obligatoire de chaque corrigé :

```python
# =============================================================================
# Corrigé — Module XN : [Titre]
# Fichier cible dans jeu/ : [nom du fichier]
# =============================================================================
#
# NIVEAU 1 — Solution minimale (le strict nécessaire pour que ça fonctionne)
# -----------------------------------------------------------------------------

... code niveau 1 ...

# NIVEAU 2 — Enrichissement (robustesse, cas limites)
# -----------------------------------------------------------------------------

... code niveau 2 ...

# NIVEAU 3 — Version complète intégrable dans jeu/ (identique ou proche
#             du code réel de jeu/)
# -----------------------------------------------------------------------------

... code niveau 3 ...
```

---

## Contenu détaillé des modules

### Phase 0 — Comprendre avant de coder

**A0 — Lire les règles, représenter le jeu**
- Objectif : l'étudiant peut décrire le jeu avec ses propres mots et
  dessiner la grille avec toutes ses entités
- Concept clé : avant de coder, modéliser — un programme est la traduction
  d'une réalité en structures formelles
- Exercice notebook : à partir de la description des règles fournie inline,
  représenter les entités sous forme de tableau (nom / rôle / caractéristiques)
- Corrigé .py : script qui affiche une grille d'exemple hardcodée avec
  toutes les entités positionnées

**A1 — Identifier les entités et leurs attributs**
- Objectif : l'étudiant peut lister les attributs de chaque entité et
  justifier leur type Python
- Concept clé : une entité = un ensemble d'attributs typés
- Exercice notebook : pour chaque entité (drone, tempête, survivant, état global),
  compléter un tableau attribut / type / valeur initiale / valeur possible
- Corrigé .py : les 3 fonctions factory `creer_drone()`, `creer_survivant()`,
  `creer_tempete()` minimales

**A2 — Choisir ses structures de données**
- Objectif : l'étudiant sait justifier le choix de dict, list, set ou tuple
  pour chaque donnée du jeu
- Concept clé : la structure de données doit correspondre à l'usage
  (accès par clé → dict, unicité → set, ordre → list, immuable → tuple)
- Exercice notebook : pour 8 cas concrets du jeu, choisir et justifier
  la structure (ex : "les positions occupées", "la liste des drones",
  "les coordonnées d'un drone")
- Risque : choisir une liste pour stocker les positions occupées → O(n)
  au lieu de O(1) avec un set, problème de performance sur grande grille
- Corrigé .py : initialisation de `etat` avec toutes ses structures

**A3 — Pseudo-code d'un tour de jeu complet**
- Objectif : l'étudiant peut écrire en français les étapes d'un tour complet,
  dans l'ordre, sans ambiguïté
- Concept clé : décomposer un processus complexe en étapes atomiques
  séquentielles avant de coder
- Exercice notebook : compléter un pseudo-code à trous (10 étapes, 4 manquantes)
- Corrigé .py : squelette de `boucle_de_jeu()` avec commentaires pseudo-code
  et `pass` à la place du vrai code

---

### Phase 1 — Liant algorithmique

**B0 — Tracer un programme à la main**
- Objectif : l'étudiant peut simuler manuellement l'exécution de
  `executer_mouvement()` en suivant l'état de `etat` pas-à-pas
- Concept clé : un programme est une séquence d'affectations et de tests ;
  tracer à la main = comprendre sans ambiguïté
- Exercice notebook : tableau de traçage avec état initial donné,
  l'étudiant remplit colonne par colonne (variable / avant / après)
- Risque : sans traçage, l'étudiant code par intuition et ne comprend
  pas pourquoi son programme ne fait pas ce qu'il croit
- Corrigé .py : `executer_mouvement()` version minimale avec
  `print()` de debug à chaque étape

---

### Phase 2 — Construire couche par couche

**P01 — config.py**
- Fichier cible : `jeu/config.py` + `jeu/config.json`
- Objectif : lire un fichier JSON et exposer des constantes nommées
- Concept clé : externaliser la configuration = zéro valeur magique dans le code
- Exercice : écrire `charger_config()`, lire `config.json`, exposer
  `GRILLE_TAILLE`, `BATTERIE_MAX`, `NB_DRONES`, etc.
- Risque : valeurs hardcodées → modifier les règles nécessite de fouiller
  tout le code

**P02 — logique.py (entités)**
- Fichier cible : `jeu/logique.py` — fonctions factory
- Objectif : coder les 3 fonctions factory et `initialiser_partie()`
- Concept clé : fonction factory = fonction qui retourne un dictionnaire
  initialisé, DRY appliqué aux structures de données
- Exercice : coder `creer_drone()`, `creer_survivant()`, `creer_tempete()`,
  puis `initialiser_partie()` avec placement aléatoire non-chevauchant
- Risque : dupliquer la structure du dict à chaque création → incohérence
  si on modifie un attribut

**P03 — affichage.py**
- Fichier cible : `jeu/affichage.py`
- Objectif : afficher une grille 2D lisible en terminal
- Concept clé : une grille = liste de listes, indexée `[lig][col]` ;
  séparer rendu et logique
- Exercice : `render_grille(etat)` affichant les symboles avec en-têtes
  colonnes (A–L) et numéros de lignes
- Risque : mélanger affichage et logique → impossible de tester la logique
  sans lancer le terminal

**P04 — logique.py (validation)**
- Fichier cible : `jeu/logique.py` — `valider_mouvement()`
- Objectif : écrire une fonction de validation pure (pas d'effet de bord)
  retournant `(bool, str)`
- Concept clé : séparer validation et exécution — une fonction qui vérifie
  ne modifie jamais l'état
- Exercice : coder `valider_mouvement()` pour les cas : hors grille,
  bâtiment, distance > 1, batterie insuffisante
- Risque : mélanger validation et exécution → impossible de vérifier
  sans modifier l'état, bugs difficiles à isoler

**P05 — logique.py (exécution nominale)**
- Fichier cible : `jeu/logique.py` — `executer_mouvement()` cas nominal
- Objectif : déplacer un drone, consommer la batterie, gérer prise
  et livraison de survivant
- Concept clé : une fonction d'exécution modifie l'état ET retourne un log ;
  le cas nominal = le chemin sans erreur
- Exercice : déplacement simple, prise de survivant, livraison à l'hôpital
- Risque : oublier de mettre à jour la grille après déplacement →
  incohérence entre `etat["drones"]` et `etat["grille"]`

**P06 — logique.py (cas limites)**
- Fichier cible : `jeu/logique.py` — collision, `hors_service`, zones X,
  propagation, phase météo
- Objectif : traiter tous les cas limites qui rendent le jeu complet
- Concept clé : les cas limites définissent la robustesse du programme ;
  ils doivent être identifiés avant de coder, pas découverts au debug
- Exercice : collision tempête (blocage 2 tours), batterie épuisée en vol
  (hors_service), entrée zone X (coût +2), `deplacer_tempetes()`,
  `propager_zones_x()`
- Risque : ignorer un cas limite → comportement indéfini en partie réelle

**P07 — console.py (J1 — drones)**
- Fichier cible : `jeu/console.py` — phase J1
- Objectif : lire une saisie clavier, la valider, l'exécuter, afficher le résultat
- Concept clé : architecture parser → valider → exécuter ; séparer
  la lecture de la saisie de son traitement
- Exercice : `phase_j1(etat)` — boucle `while nb_depl < MAX`,
  `input()`, `position_depuis_chaine()`, appel `valider_mouvement()` +
  `executer_mouvement()`
- Risque : traiter la saisie directement sans parser → code non réutilisable,
  bugs de format difficiles à corriger

**P08 — console.py (J2 — tempêtes + météo)**
- Fichier cible : `jeu/console.py` — phase J2 + météo automatique
- Objectif : gérer le deuxième joueur et la phase automatique de fin de tour
- Concept clé : un tour de jeu = J1 + J2 + automatique ; chaque phase
  est une fonction distincte
- Exercice : `phase_j2(etat)`, puis `fin_de_tour(etat)` incluant
  `deplacer_tempetes()`, `propager_zones_x()`, `verifier_fin_partie()`
- Risque : imbriquer les phases dans une seule fonction → impossible de
  tester J1 sans J2

**P09 — main.py (assemblage final)**
- Fichier cible : `jeu/main.py`
- Objectif : assembler tous les modules en un programme jouable
- Concept clé : `main.py` ne contient aucune logique — il orchestre ;
  `if __name__ == '__main__'` isole l'exécution de l'import
- Exercice : écrire `main()` appelant `demarrer_log()`,
  `initialiser_partie()`, `boucle_de_jeu(etat)` ; tester une partie complète
- Risque : mettre de la logique dans `main.py` → couplage fort,
  impossible à tester unitairement

---

### Phase 3 — Savoirs transversaux

**C0 — Architecture multi-fichiers**
- Objectif : comprendre pourquoi et comment découper un programme en modules
- Concept clé : une responsabilité par fichier ; graphe de dépendances
  à sens unique (main → console → logique/affichage ; jamais l'inverse)
- Exercice notebook : dessiner le graphe de dépendances du projet,
  identifier les violations potentielles
- Lien : `REFERENTIEL_ENSEIGNEMENTS.md` section "Multi-fichiers"

**C1 — Configuration externe**
- Objectif : comprendre pourquoi toutes les constantes sont dans `config.json`
- Concept clé : DRY appliqué aux données, maintenabilité, séparation
  code/configuration
- Exercice notebook : partir d'un code avec 5 valeurs magiques,
  les externaliser dans un dict puis dans un JSON
- Lien : `jeu/config.json` + `jeu/config.py`

**C2 — Déboguer avec le logger**
- Objectif : savoir lire une stack trace, utiliser `print()` et le logger
  comme outils de débogage
- Concept clé : un bug = un écart entre l'état attendu et l'état réel ;
  le logger matérialise l'état à chaque étape
- Exercice notebook : à partir d'un code bugué fourni (3 bugs intentionnels),
  utiliser le logger pour les identifier
- Lien : `jeu/logger.py`

**C3 — Versionner avec Git**
- Objectif : faire un commit atomique par étape fonctionnelle,
  lire un diff, consulter l'historique
- Concept clé : un commit = un état stable et documenté du programme,
  pas juste une sauvegarde
- Exercice notebook : simulation textuelle d'un workflow Git
  (init → add → commit → log → diff)
- Lien : `GIT_BASH_GUIDE.md` existant dans le repo

**C4 — Tester ses fonctions**
- Objectif : écrire des tests simples pour `valider_mouvement()`
  et `creer_drone()` sans lancer le jeu
- Concept clé : tester = appeler une fonction avec un état contrôlé
  et vérifier le résultat avec `assert`
- Exercice notebook : 5 cas de test à écrire (2 cas valides,
  3 cas invalides) pour `valider_mouvement()`
- Lien : `tests/` existant dans le repo

---

## Fichier `formation/README.md` à produire

Ce fichier doit contenir :
1. Présentation du parcours (objectif global, public, durée totale estimée)
2. Tableau de tous les modules (phase / id / titre / durée / prérequis /
   fichier cible dans jeu/)
3. Comment utiliser les 3 types de fichiers (.md, .ipynb, .py) ensemble
4. Prérequis techniques (Python 3.10+, Jupyter ou Google Colab, Git)
5. Lien vers `jeu/` comme destination finale du parcours
6. Lien vers les ressources existantes (`cours/`, `exercices/`,
   `REFERENTIEL_ENSEIGNEMENTS.md`, `GUIDE_FORMATEUR.md`)

---

## Consignes de style et de langue

- **Tout en français** : code, commentaires, docstrings, markdown, notebooks
- **Ton pédagogique** : bienveillant, direct, sans jargon inutile
- **Exemples concrets** : toujours tirés du jeu Drone Rescue, jamais abstraits
- **Code** : PEP 8, snake_case, constantes en MAJUSCULES, docstrings sur
  toutes les fonctions, pas de valeurs magiques
- **Notebooks** : une cellule = un objectif clair affiché en Markdown
  avant la cellule de code ; cellules `assert` de vérification après
  chaque étape clé
- **Corrigés** : 3 niveaux progressifs clairement séparés par des
  commentaires de section

---

## Ordre de production recommandé

1. `formation/README.md` (vue d'ensemble)
2. Phase 0 complète (A0 → A3) — pose les fondations conceptuelles
3. Phase 1 (B0) — liant algorithmique
4. Phase 2 dans l'ordre (P01 → P09) — construction incrémentale
5. Phase 3 (C0 → C4) — consolidation transversale

Chaque module doit être produit dans l'ordre : `.md` → `.ipynb` → `_corrige.py`

---

*Ce prompt a été rédigé le 2026-04-01 par Stéphane Magnand (contributeur)
dans le cadre du projet pédagogique Drone Rescue — Kedge / ISAE.*
