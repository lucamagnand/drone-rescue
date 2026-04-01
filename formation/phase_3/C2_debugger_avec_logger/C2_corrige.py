# =============================================================================
# C2_corrige.py — Déboguer avec le logger
# Trois niveaux de maîtrise
# =============================================================================

import io
from datetime import datetime

# ---------------------------------------------------------------------------
# NIVEAU 1 — Reproduction fidèle du logger de Drone Rescue (en mémoire)
# ---------------------------------------------------------------------------

NIVEAUX = {"DEBUG": 0, "INFO": 1, "AVERT": 2, "ERREUR": 3}


class LoggerSimple:
    """Logger minimal calqué sur jeu/logger.py, sans fichier disque."""

    def __init__(self):
        self._buf = io.StringIO()

    def demarrer(self):
        self._buf.seek(0)
        self._buf.truncate()
        self._buf.write("=== DRONE RESCUE — Journal de partie ===\n")
        self._buf.write("Tour | Entité | Mouvement | Événement\n")
        self._buf.write("-" * 50 + "\n")

    def enregistrer(self, ligne: str):
        self._buf.write(ligne + "\n")

    def contenu(self) -> str:
        return self._buf.getvalue()


# ---------------------------------------------------------------------------
# NIVEAU 2 — Logger avec horodatage et niveaux de sévérité
# ---------------------------------------------------------------------------


class LoggerAvance:
    """Logger avec timestamp, niveaux et filtre dynamique."""

    def __init__(self, seuil: str = "INFO"):
        self._buf = io.StringIO()
        self.seuil = seuil

    def demarrer(self):
        self._buf.seek(0)
        self._buf.truncate()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._buf.write(f"=== DRONE RESCUE — Log démarré le {ts} ===\n")
        self._buf.write(f"Seuil actif : {self.seuil}\n")
        self._buf.write("-" * 60 + "\n")

    def enregistrer(self, niveau: str, ligne: str):
        """N'écrit que si niveau >= seuil configuré."""
        if NIVEAUX.get(niveau, 0) >= NIVEAUX.get(self.seuil, 0):
            ts = datetime.now().strftime("%H:%M:%S")
            self._buf.write(f"[{ts}][{niveau:<6}] {ligne}\n")

    def lire_par_niveau(self, niveau: str) -> list[str]:
        """Retourne uniquement les lignes du niveau demandé."""
        self._buf.seek(0)
        return [l.strip() for l in self._buf if f"[{niveau}" in l]

    def bilan(self) -> dict:
        """Statistiques par niveau."""
        self._buf.seek(0)
        lignes = self._buf.readlines()
        return {
            nv: sum(1 for l in lignes if f"[{nv}" in l)
            for nv in NIVEAUX
        }

    def contenu(self) -> str:
        return self._buf.getvalue()


# ---------------------------------------------------------------------------
# NIVEAU 3 — Logger avec rotation (simulation taille max)
# ---------------------------------------------------------------------------


class LoggerAvecRotation(LoggerAvance):
    """
    Variante qui simule la rotation :
    quand le buffer dépasse max_lignes événements,
    les plus anciennes sont supprimées.
    """

    def __init__(self, seuil: str = "INFO", max_lignes: int = 50):
        super().__init__(seuil)
        self.max_lignes = max_lignes
        self._lignes: list[str] = []

    def enregistrer(self, niveau: str, ligne: str):
        if NIVEAUX.get(niveau, 0) >= NIVEAUX.get(self.seuil, 0):
            ts = datetime.now().strftime("%H:%M:%S")
            entree = f"[{ts}][{niveau:<6}] {ligne}"
            self._lignes.append(entree)
            if len(self._lignes) > self.max_lignes:
                # On garde les max_lignes les plus récentes
                self._lignes = self._lignes[-self.max_lignes:]

    def contenu(self) -> str:
        return "\n".join(self._lignes) + "\n"


# ---------------------------------------------------------------------------
# Démonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    log = LoggerAvance(seuil="INFO")
    log.demarrer()
    log.enregistrer("DEBUG",  "calcul interne ignoré")
    log.enregistrer("INFO",   "Tour 1 : drone_1 → N")
    log.enregistrer("AVERT",  "batterie drone_2 < 20 %")
    log.enregistrer("ERREUR", "collision détectée case (3,3)")
    log.enregistrer("INFO",   "Tour 2 : drone_1 → E, survivant S1 sauvé")

    print(log.contenu())
    print("Bilan :", log.bilan())
    print("\nLignes ERREUR :")
    for l in log.lire_par_niveau("ERREUR"):
        print(" ", l)
