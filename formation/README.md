# Formation Drone Rescue — Parcours guidé

> **Objectif** : partir de zéro et construire, étape par étape, le code complet
> du jeu Drone Rescue situé dans `jeu/`.
> Public cible : étudiants en 1ère année d'école d'ingénieurs, aucune
> expérience de programmation requise.

---

## Comment utiliser ce parcours

`formation/` est le **parcours pédagogique canonique** : il structure l'ensemble de l'apprentissage,
du premier contact avec le jeu jusqu'à l'écriture complète du code source.

Les dossiers `cours/`, `notebooks/`, `exercices/`, `corrections/` et `tests/` sont des
**ressources satellites** : chaque module de ce parcours indique dans sa section
« Ressources associées » quels fichiers consulter et à quel moment.

> 📖 **Étudiant** → commence ici, module par module, dans l'ordre du tableau.
> 🏫 **Formateur** → commence par `GUIDE_FORMATEUR.md` pour le calage pédagogique.

**Durée totale estimée : 25 à 30 heures** (selon le rythme de l'étudiant)

---

## Convention des 4 temps par module

Chaque module suit la même séquence :

| Étape | Fichier | Action |
|---|---|---|
| 📖 **Lire** | `XN.md` | Comprendre le concept, les risques, le lien avec `jeu/` |
| ⚙️ **Pratiquer** | `XN.ipynb` | Compléter les `TODO`, vérifier avec les `assert` |
| ✅ **Comparer** | `XN_corrige.py` | Consulter le corrigé après avoir essayé |
| 🔍 **Approfondir** | ressources associées | Cours, exercices, notebooks, corrections selon le module |

**Flux recommandé :**
```
Lire XN.md → Ouvrir XN.ipynb → Compléter les TODO → Vérifier avec assert → Comparer avec XN_corrige.py
```

> ⚠️ Ne pas ouvrir le corrigé avant d'avoir essayé. La lutte cognitive est le moteur de l'apprentissage.

---

## Prérequis techniques

- Python 3.10 ou supérieur installé
- Jupyter Notebook **ou** accès à [Google Colab](https://colab.research.google.com)
  (tous les notebooks sont compatibles Colab — aucun fichier local requis)
- Git installé (pour la Phase 3 / C3) — voir `GIT_BASH_GUIDE.md`
- Un éditeur de texte (VS Code recommandé) ou un terminal

---

## Tableau des modules

| Phase | ID | Titre | Durée | Prérequis | Fichier cible `jeu/` |
|---|---|---|---|---|---|
| **Phase 0** | A0 | Lire les règles, représenter le jeu | 30 min | — | *(aucun)* |
| **Phase 0** | A1 | Identifier les entités et leurs attributs | 45 min | A0 | `logique.py` |
| **Phase 0** | A2 | Choisir ses structures de données | 45 min | A1 | `logique.py` |
| **Phase 0** | A3 | Pseudo-code d'un tour de jeu complet | 60 min | A0–A2 | `console.py` |
| **Phase 1** | B0 | Tracer un programme à la main | 60 min | A0–A3 | `logique.py` |
| **Phase 1** | B1 | Simuler des fonctions à la main | 45 min | B0 | `logique.py` |
| **Phase 1** | B2 | Repérer les cas limites avant de coder | 45 min | B1 | `logique.py` |
| **Phase 2** | P01 | `config.py` — lire la configuration | 45 min | A2 | `config.py`, `config.json` |
| **Phase 2** | P02 | `logique.py` — fonctions factory | 60 min | A1, P01 | `logique.py` |
| **Phase 2** | P03 | `affichage.py` — rendu de la grille | 45 min | A0, P02 | `affichage.py` |
| **Phase 2** | P04 | `logique.py` — validation de mouvement | 60 min | B2, P02 | `logique.py` |
| **Phase 2** | P05 | `logique.py` — exécution nominale | 60 min | P04 | `logique.py` |
| **Phase 2** | P06 | `logique.py` — cas limites | 90 min | P05 | `logique.py` |
| **Phase 2** | P07 | `console.py` — phase J1 (drones) | 60 min | P04, P05 | `console.py` |
| **Phase 2** | P08 | `console.py` — phase J2 + météo | 60 min | P07, P06 | `console.py` |
| **Phase 2** | P09 | `main.py` — assemblage final | 45 min | P01–P08 | `main.py` |
| **Phase 3** | C0 | Architecture multi-fichiers | 30 min | P09 | *(transversal)* |
| **Phase 3** | C1 | Configuration externe | 30 min | P01 | `config.json` |
| **Phase 3** | C2 | Déboguer avec le logger | 50 min | C1, P08 | `logger.py` |
| **Phase 3** | C3 | Versionner avec Git | 45 min | P09 | *(transversal)* |
| **Phase 3** | C4 | Tester ses fonctions | 45 min | P04 | `tests/` |

---

## Structure du dossier

```
formation/
├── README.md                        ← ce fichier
├── phase_0/
│   ├── A0_regles_et_representation/
│   ├── A1_entites_et_attributs/
│   ├── A2_choix_structures_donnees/
│   └── A3_pseudocode_tour_de_jeu/
├── phase_1/
│   ├── B0_tracer_a_la_main/
│   ├── B1_simuler_fonctions_a_la_main/     ← à créer
│   └── B2_reperer_cas_limites/             ← à créer
├── phase_2/
│   ├── P01_config/
│   ├── P02_entites/
│   ├── P03_affichage/
│   ├── P04_validation/
│   ├── P05_execution_nominal/
│   ├── P06_cas_limites/
│   ├── P07_console_j1/
│   ├── P08_console_j2/
│   └── P09_assemblage/
└── phase_3/
    ├── C0_architecture_multifichiers/
    ├── C1_configuration_externe/
    ├── C2_deboguer_avec_logger/
    ├── C3_versionner_avec_git/
    └── C4_tester_ses_fonctions/
```

---

## Ressources satellites (ne pas utiliser comme point d'entrée)

Ces dossiers sont **appelés depuis chaque module** via la section « Ressources associées ».
Ne pas les parcourir indépendamment sans suivre le parcours.

| Ressource | Utilité |
|---|---|
| `cours/` | 10 modules de cours théoriques (00 → 09) |
| `exercices/` | 9 exercices `.py` (ex_01 → ex_09) |
| `corrections/` | Corrigés des exercices |
| `notebooks/` | Notebooks Jupyter complémentaires |
| `REFERENTIEL_ENSEIGNEMENTS.md` | Référentiel complet des notions Python du jeu |
| `GUIDE_FORMATEUR.md` | Guide pédagogique pour l'enseignant |
| `GIT_BASH_GUIDE.md` | Guide Git pour les étudiants |

---

## Destination finale

À l'issue du parcours, l'étudiant aura écrit **l'intégralité du code** présent
dans le dossier `jeu/` :

```
jeu/
├── main.py       ← P09
├── logique.py    ← P02, P04, P05, P06
├── console.py    ← P07, P08
├── affichage.py  ← P03
├── config.py     ← P01
├── config.json   ← P01, C1
└── logger.py     ← C2
```

Bonne progression ! 🚁
