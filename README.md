# 🚁 Drone Rescue — Cours Python par projet

> Projet pédagogique : développer un jeu de simulation de sauvetage par drones, en Python console, sur 6 semaines.

## Objectif

Apprendre Python de manière progressive en construisant un jeu complet :
- Grille ASCII 12×12 (colonnes A–L, lignes 1–12)
- Drones (D1–D3) et Tempêtes (T1–T2) déplacés par dictionnaires
- Console de pilotage 2 joueurs (drones vs tempêtes)
- Tableau de bord, historique, fichier de log et bilan final

## Prérequis

- Python 3.10 ou supérieur
- Un terminal (PowerShell, bash, zsh…)
- Aucune bibliothèque externe (stdlib uniquement)

## Lancer le jeu

```bash
cd drone-rescue
python jeu/main.py
```

## Structure du repo

```
drone-rescue/
├── README.md
├── ROADMAP.md
├── CHANTIER_CODE.md
├── CHANGELOG.md
├── REFERENTIEL_ENSEIGNEMENTS.md    ← référentiel complet des notions Python
├── GUIDE_FORMATEUR.md              ← guide pédagogique pour l'enseignant
├── GIT_BASH_GUIDE.md               ← guide Git pour les étudiants
├── AUDIT.md
├── BUG.md
├── _meta/                          ← documents internes formateur (non destinés aux étudiants)
│   └── PROMPT_FORMATION.md
├── formation/                      ← ★ POINT D'ENTRÉE ÉTUDIANT ★
│   ├── README.md                   ← vue d'ensemble du parcours
│   ├── phase_0/   A0 A1 A2 A3      ← Analyser avant de coder
│   ├── phase_1/   B0 B1 B2         ← Raisonner et tracer
│   ├── phase_2/   P01 → P09        ← Construire couche par couche
│   └── phase_3/   C0 → C4         ← Consolider (architecture, git, tests)
├── cours/                          ← fiches de cours (ressource satellite)
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
├── exercices/                      ← énoncés d'exercices (ex_01 à ex_09)
├── corrections/                    ← corrigés exécutables avec assert
├── notebooks/                      ← notebooks Jupyter
├── tests/                          ← tests unitaires pytest
└── jeu/                            ← code final complet jouable
    ├── config.json                 ← paramètres du jeu (source de vérité)
    ├── config.py                   ← lecture config.json + constantes
    ├── logique.py                  ← toutes les règles (dicts, sans POO)
    ├── affichage.py                ← rendu console
    ├── console.py                  ← boucle J1/J2 + saisie joueurs
    ├── logger.py                   ← partie.log + resultats.txt
    └── main.py                     ← point d'entrée
```

> **Note** : le projet n'utilise **pas** la POO — toutes les entités sont des dictionnaires Python (conformément aux contraintes du sujet).

## Parcours de formation

Le point d'entrée étudiant est **`formation/README.md`**. Le parcours se déroule en 4 phases :

| Phase | Modules | Thème | Durée |
|---|---|---|---|
| **0 — Analyser** | A0 A1 A2 A3 | Règles, entités, structures de données, pseudo-code | ~3h |
| **1 — Raisonner** | B0 B1 B2 | Traçage algorithmique, simulation, cas limites | ~2h |
| **2 — Implémenter** | P01 → P09 | config → entités → affichage → validation → exécution → console → main | ~9h |
| **3 — Consolider** | C0 → C4 | Architecture, config externe, logger, Git, tests | ~4h |

Chaque module contient : `.md` (concept) + `.ipynb` (exercice guidé) + `_corrige.py` (3 niveaux progressifs).

## Feuille de route (6 semaines)

| Semaine | Modules | Thème |
|---|---|---|
| 1 | A0–A3 + B0 | Analyse, modélisation, traçage |
| 2 | B1–B2 + P01–P02 | Cas limites, config, entités |
| 3 | P03–P05 | Affichage, validation, exécution nominale |
| 4 | P06–P08 | Cas limites, console J1/J2 |
| 5 | P09 + C0–C2 | Assemblage, architecture, logger |
| 6 | C3–C4 | Git, tests |

## Règles du jeu (résumé)

- **Plateau** : grille 12×12, coordonnées colonne (A–L) × ligne (1–12)
- **Hôpital** : placé aléatoirement, destination de livraison des survivants
- **Drones** : 3 drones (D1–D3), batterie max configurable, déplacement diagonal autorisé (distance Chebyshev ≤ 1), 3 déplacements max par tour
- **Tempêtes** : 2 tempêtes (T1–T2), 2 déplacements max par tour, bloquent les drones 2 tours
- **Coûts** : déplacement normal −1 bat, transport survivant −1 bat supplémentaire, entrée zone X −2 bat supplémentaire
- **Recharge** : +3 batterie si drone stationnaire ou arrivant à l'hôpital
- **Zones dangereuses** : propagation probabiliste configurable
- **Fin de partie** : tous les survivants secourus (victoire) OU tous les drones hors service OU tours max dépassés (défaite)

## Convention de log

```
T[nn]  [ID]  [départ]→[arrivée]  bat:x→y  [ÉVÈNEMENT]
```

Exemple :
```
T04  D3   B7→C8   bat:6→5
T04  D2   D5→D5   bat:8→8  BLOQUE(T2)
T05  D1   E7→A10  bat:5→6  S3  LIVRAISON S3 +1pt
```
