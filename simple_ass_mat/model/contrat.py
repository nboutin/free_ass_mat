"""
Author: Nicolas Boutin
Date: 2023-08
Description: Represent contrat entre parent employeur et ass.mat.
"""


from .remuneration import Remuneration
from .planning import Planning


class Contrat:
    """Contrat pour un enfant entre parent employeur et ass.mat."""

    def __init__(self, planning: Planning, remuneration: Remuneration) -> None:
        self._planning = planning
        self._remuneration = remuneration

    def get_duree_acceuil_hebdomadaire_moyen(self) -> float:
        """Return la durée hebdomadaire d'acceuil moyen

        = nombre heure semaine * nombre semaine acceuil / 52
        """
        return self._planning.get_nombre_heure_semaine() * self._planning.get_nombre_semaine_acceuil() / 52
