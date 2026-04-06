# Guide formateur — Drone Rescue Python

> Mise à jour : 6 avril 2026

---

## Présentation du projet

Drone Rescue est un **jeu de plateau pédagogique en Python**.
Deux joueurs s'affrontent : J1 déplace des drones de secours, J2 déplace des tempêtes.
Le but de J1 est de sauver tous les survivants avant la fin du nombre de tours.

### Principes pédagogiques fondamentaux

- **Zéro POO** : toutes les entités sont des **dictionnaires** (drone, tempête, survivant, état global)
- **Fonctions fabriquantes** à la place de classes : `creer_drone()`, `creer_tempete()`, `creer_survivant()`
- **Coordonnées 0-based en interne** : `col` et `lig` sont des entiers commençant à 0
- **Notation affichage 1-based** : `A1` = `(col=0, lig=0)`, `B3` = `(col=1, lig=2)`
- Stdlib Python uniquement — compatible Google Colab sans installation

---

## Architecture du repo

```
drone-rescue/
├── jeu/                  Moteur du jeu (ne pas modifier sans raison)
│   ├── config.py         Paramètres officiels (TAILLE, COUT, NB_DRONES…)
│   ├── config.json       Même paramètres au format JSON
│   ├── logique.py        Règles : validation, exécution, propagation, fin de partie
│   ├── affichage.py      Rendu ASCII 3 colonnes (grille | statuts | log)
│   ├── console.py        Boucle de jeu, saisie J1/J2, architecture parser→valider→exécuter
│   ├── logger.py         Journalisation fichier (partie.log, resultats.txt)
│   └── main.py           Point d'entrée : python main.py
├── formation/            ← Parcours pédagogique canonique (point d'entrée étudiants)
├── cours/                10 fichiers .md — ressource satellite de formation/
├── exercices/            ex_01.py → ex_09_assemblage.py — ressource satellite
├── corrections/          corr_01.py → corr_09_assemblage.py — ressource satellite
├── notebooks/            nb_01 → nb_09 — ressource satellite
└── tests/                test_logique.py (pytest — validation du moteur)
```

> Les dossiers `cours/`, `exercices/`, `corrections/`, `notebooks/` sont des **ressources satellites**.
> Chaque module de `formation/` indique dans sa section « Ressources associées » quels fichiers utiliser.
> Ne pas demander aux étudiants de parcourir ces dossiers indépendamment.

---

## Parcours pédagogique

### Point d'entrée unique : `formation/README.md`

Le parcours est découpé en 4 phases :

| Phase | ID | Titre | Objectif |
|---|---|---|---|
| **Phase 0 — Analyser** | A0–A3 | Règles, entités, structures, pseudo-code | Comprendre le jeu sans coder |
| **Phase 1 — Raisonner** | B0–B2 | Tracer, simuler, cas limites | Penser comme le programme |
| **Phase 2 — Implémenter** | P01–P09 | Fichier par fichier jusqu'à `main.py` | Produire le code du jeu |
| **Phase 3 — Consolider** | C0–C4 | Architecture, config, debug, git, tests | Solidifier et professionnaliser |

### La Phase 1 est la charnère cognitive

La Phase 1 (B0–B2) est le moment où l'étudiant apprend à **raisonner comme un programme** avant de coder.
C'est souvent la phase la plus négligée, et la plus déterminante pour la suite.

| Module | Objectif spécifique |
|---|---|
| B0 — Tracer à la main | Suivre l'état du programme pas à pas, sans exécuter |
| B1 — Simuler des fonctions | Donner des entrées, calculer la sortie attendue à la main |
| B2 — Repérer les cas limites | Anticiper les valeurs à la frontière : grille, batterie, collision |

---

## Paramètres officiels du jeu

| Paramètre | Valeur | Fichier |
|-----------|--------|---------|
| Taille grille | **12×12** | `config.py` / `config.json` |
| Colonnes | A → L (12 lettres) | affichage |
| Lignes | 1 → 12 | affichage |
| Nombre de drones | 6 | `config.py` |
| Nombre de tempêtes | 4 | `config.py` |
| Nombre de survivants | 10 | `config.py` |
| Bâtiments | ~20 (aléatoire) | `config.py` |
| Batterie initiale | 10 | `config.py` |
| Batterie max | 20 | `config.py` |
| Coût déplacement normal | 1 | `config.py` |
| Coût transport survivant | 2 | `config.py` |
| Coût zone X (supplément) | 2 | `config.py` |
| Recharge hôpital | 3 | `config.py` |
| Nombre de tours max | 20 | `config.py` |
| Déplacements J1/tour | 3 | `config.py` |
| Déplacements J2/tour | 2 | `config.py` |
| Hôpital | aléatoire | `logique.py` |

---

## Convention coordonnées — point critique

C'est le point le plus source de confusion pour les apprenants :

```python
# INTERNE (code) — entiers 0-based
col: int   # 0 = colonne A,  11 = colonne L  (grille 12x12)
lig: int   # 0 = ligne 1,   11 = ligne 12

# AFFICHAGE (cours, exercices, log) — lettre + numéro 1-based
# Exemples :
#   (col=0,  lig=0)  → 'A1'
#   (col=1,  lig=2)  → 'B3'
#   (col=11, lig=11) → 'L12'

# Conversion :
col = LETTRES.index(lettre)   # 'B'  → 1
lig = num - 1                 # 3    → 2
```

> ⚠️ Dans les exercices et notebooks, toujours utiliser la notation affichage (`B3`).
> Le moteur gère la conversion en interne.

---

## Lancer le jeu

```bash
cd jeu
python main.py
```

### Commandes en jeu

| Saisie | Effet |
|--------|-------|
| `D1` puis `B3` | Déplace le drone D1 vers la case B3 |
| `T1` puis `E5` | Déplace la tempête T1 vers E5 |
| `next` | Passe à la phase suivante |
| `q` | Quitte la partie |

---

## Lancer les tests

```bash
pip install pytest
pytest tests/test_logique.py -v
```

Ou sans pytest (assertions directes) :

```bash
python tests/test_logique.py
```

---

## Points d'attention pour les formateurs

### ❌ À ne pas faire
- Ne pas introduire de classes (`class Drone`) — le projet est volontairement sans POO
- Ne pas utiliser `ord()`/`chr()` pour les conversions de colonnes — utiliser `LETTRES.index()` et `LETTRES[col]`
- Ne pas mélanger coordonnées 0-based et 1-based dans les exemples
- Ne pas demander aux étudiants de consulter `cours/` ou `exercices/` directement — les référer via les modules `formation/`

### ✅ Bonnes pratiques à montrer
- Fonctions fabriquantes avec `return {…}` (pattern dict-as-object)
- `all()` / `any()` sur des générateurs dict
- `f"{LETTRES[col]}{lig + 1}"` pour l'affichage
- Architecture parser → valider → exécuter dans les boucles de saisie

### Erreurs classiques des apprenants
- Confondre `grille[lig][col]` avec `grille[col][lig]` (lignes d'abord !)
- Oublier le `+ 1` dans l'affichage ou le `- 1` dans le parsing
- Modifier un dict sans vérifier la validité du mouvement d'abord
- Rester bloqué en Phase 1 (B0–B2) par manque de confiance : les encourager à tracer sur papier

---

## Fichiers à ne pas modifier sans raison

- `jeu/config.py` et `jeu/config.json` — les paramètres officiels sont figés
- `jeu/logique.py` — le moteur est validé par les tests
- `corrections/` — référence pour l'évaluation

*MAJ : 6 avril 2026 — grille 12×12, parcours canonique formation/, Phase 1 B0–B2.*
