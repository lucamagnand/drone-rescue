# =============================================================================
# C3_corrige.py — Versionner avec Git
# Simulation d'un dépôt Git en Python pur
# Trois niveaux de maîtrise
# =============================================================================

from datetime import datetime
import hashlib


# ---------------------------------------------------------------------------
# NIVEAU 1 — Dépôt minimal : add, commit, log
# ---------------------------------------------------------------------------


class Commit:
    """Représente un instantané (snapshot) de l'état des fichiers."""

    def __init__(self, message: str, fichiers: dict, parent=None):
        self.message = message
        self.fichiers = dict(fichiers)
        self.parent = parent
        self.horodatage = datetime.now().isoformat()
        # SHA déterministe basé sur message + contenu
        contenu_sha = str(sorted(fichiers.items())) + message + self.horodatage
        self.sha = hashlib.sha1(contenu_sha.encode()).hexdigest()[:8]

    def __repr__(self) -> str:
        return f"Commit({self.sha!r}, {self.message!r})"


class DepotMinimal:
    """Dépôt Git simplifié : add + commit + log."""

    def __init__(self):
        self.commits: list[Commit] = []
        self.staging: dict[str, str] = {}
        self.working: dict[str, str] = {}

    def modifier_fichier(self, nom: str, contenu: str):
        self.working[nom] = contenu

    def add(self, nom: str = "."):
        """Stage un fichier (ou tous si nom='.')."""
        if nom == ".":
            self.staging.update(self.working)
        elif nom in self.working:
            self.staging[nom] = self.working[nom]
        else:
            print(f"pathspec '{nom}' ne correspond à aucun fichier")

    def commit(self, message: str) -> Commit | None:
        if not self.staging:
            print("rien à committer, l'index est vide")
            return None
        parent = self.commits[-1] if self.commits else None
        c = Commit(message, self.staging, parent)
        self.commits.append(c)
        self.staging = {}
        print(f"[{c.sha}] {message}")
        return c

    def log(self):
        if not self.commits:
            print("Aucun commit.")
            return
        for c in reversed(self.commits):
            print(f"{c.sha}  {c.horodatage[:19]}  {c.message}")


# ---------------------------------------------------------------------------
# NIVEAU 2 — Diff, status, branches
# ---------------------------------------------------------------------------


class DepotAvance(DepotMinimal):
    """Ajoute diff, status et gestion de branches."""

    def __init__(self):
        super().__init__()
        self.branches: dict[str, list[Commit]] = {"main": []}
        self.branche_courante: str = "main"

    def commit(self, message: str) -> Commit | None:
        c = super().commit(message)
        if c:
            self.branches[self.branche_courante].append(c)
        return c

    def checkout_b(self, nom: str):
        """Crée une nouvelle branche à partir de l'état courant."""
        self.branches[nom] = list(self.commits)
        self.branche_courante = nom
        print(f"Basculé sur la nouvelle branche '{nom}'")

    def status(self):
        """Affiche l'état du dépôt (staged vs non-staged)."""
        print(f"Sur la branche {self.branche_courante}")
        snapshot = self.commits[-1].fichiers if self.commits else {}

        stagues = list(self.staging.keys())
        non_stagues = [
            f for f, v in self.working.items()
            if v != snapshot.get(f) and f not in self.staging
        ]
        non_suivi = [
            f for f in self.working
            if f not in snapshot and f not in self.staging
        ]

        if stagues:
            print("\nChangements qui seront commités :")
            for f in stagues:
                print(f"  modifié : {f}")
        if non_stagues:
            print("\nChangements non indexés :")
            for f in non_stagues:
                print(f"  modifié : {f}")
        if non_suivi:
            print("\nFichiers non suivis :")
            for f in non_suivi:
                print(f"  {f}")
        if not stagues and not non_stagues and not non_suivi:
            print("rien à committer, la copie de travail est propre")

    def diff(self, sha_a: str = None, sha_b: str = None):
        """Diff entre deux commits (SHA) ou HEAD et staging."""
        def trouver(sha):
            for c in self.commits:
                if c.sha == sha:
                    return c
            return None

        if sha_a and sha_b:
            ca, cb = trouver(sha_a), trouver(sha_b)
            if not ca or not cb:
                print("SHA introuvable.")
                return
            f_a, f_b = ca.fichiers, cb.fichiers
        else:
            f_a = self.commits[-1].fichiers if self.commits else {}
            f_b = self.staging

        tous = set(f_a) | set(f_b)
        for f in sorted(tous):
            avant = f_a.get(f, "(absent)")
            apres = f_b.get(f, "(absent)")
            if avant != apres:
                print(f"diff {f}")
                print(f"-  {avant}")
                print(f"+  {apres}")


# ---------------------------------------------------------------------------
# NIVEAU 3 — Merge (fast-forward simulé)
# ---------------------------------------------------------------------------


class DepotComplet(DepotAvance):
    """Ajoute un merge fast-forward simplifié."""

    def merge(self, branche_source: str):
        """Fusionne branche_source dans la branche courante."""
        if branche_source not in self.branches:
            print(f"branche '{branche_source}' introuvable")
            return
        commits_source = self.branches[branche_source]
        commits_courant = set(c.sha for c in self.branches[self.branche_courante])

        nouveaux = [c for c in commits_source if c.sha not in commits_courant]
        if not nouveaux:
            print("Déjà à jour.")
            return

        for c in nouveaux:
            self.commits.append(c)
            self.branches[self.branche_courante].append(c)

        print(
            f"Merge fast-forward : {len(nouveaux)} commit(s) de "
            f"'{branche_source}' → '{self.branche_courante}'"
        )


# ---------------------------------------------------------------------------
# Démonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    d = DepotComplet()

    d.modifier_fichier("main.py", "print('v1')")
    d.add()
    d.commit("init : main.py v1")

    d.checkout_b("marie-exercices")
    d.modifier_fichier("ex01.py", "def somme(a, b): return a + b")
    d.add()
    d.commit("ex01 : fonction somme")

    d.modifier_fichier("ex01.py", "def somme(a, b): return a + b  # v2")
    d.add()
    d.commit("ex01 : commentaire ajouté")

    print("\n--- log branche marie-exercices ---")
    d.log()

    print("\n--- merge dans main ---")
    # Revenir sur main (simulation)
    d.branche_courante = "main"
    d.merge("marie-exercices")

    print("\n--- log main après merge ---")
    d.log()

    print("\n--- status ---")
    d.modifier_fichier("ex02.py", "nouveau fichier")
    d.status()
