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
├── exercices/                  ← 9 exercices .py existants (ex_01 → ex_09)
├── corrections/                ← corrigés des exercices existants
├── notebooks/                  ← notebooks Jupyter existants
├── tests/                      ← tests unitaires existants
├── formation/                  ← parcours pédagogique canonique (point d'entrée étudiants)
├── REFERENTIEL_ENSEIGNEMENTS.md
├── GUIDE_FORMATEUR.md
└── GIT_BASH_GUIDE.md
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
    "zones_x": {(col, lig), ...},
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
├── README.md
├── phase_0/   A0 A1 A2 A3
├── phase_1/   B0 B1 B2
├── phase_2/   P01→P09
└── phase_3/   C0→C4
```

Chaque module : `XN.md` + `XN.ipynb` + `XN_corrige.py`

---

## Contenu détaillé des modules

*(voir version complète originale — contenu identique, fichier déplacé dans `_meta/` pour ne pas être visible des étudiants)*

---

*Ce prompt a été rédigé le 2026-04-01 par Stéphane Magnand (contributeur)
dans le cadre du projet pédagogique Drone Rescue — Kedge / ISAE.*
