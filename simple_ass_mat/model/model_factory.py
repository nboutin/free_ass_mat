"""
Author: Nicolas Boutin
Date: 2023-08
Description:
"""

from copy import deepcopy
from datetime import time

from .data_loader import IDataLoader
from .contrat import Contrat
from .remuneration import Remuneration
from .planning import Planning, SemaineAcceuil, JourAcceuil, CreneauHoraire


class ModelFactory:
    """Model Factory"""

    def __init__(self, data_loader: IDataLoader):
        self._data_loader = data_loader

    def make_contrat(self) -> Contrat:
        """Make contrat"""
        remuneration = self._make_remuneration(self._data_loader.get_remuneration_data())
        planning = self._make_planning()
        return Contrat(planning=planning, remuneration=remuneration)

    def _make_remuneration(self, remuneration_data) -> Remuneration:
        """Make Remuneration"""
        return Remuneration(salaire_horaire_brut=remuneration_data["salaire_horaire_brut"])

    def _make_planning(self) -> Planning:
        """Make planning"""

        semaines_acceuil = {}
        semaines_presences_data = self._data_loader.get_semaines_presences_data()

        for semaine_id, numero_semaines_list in semaines_presences_data.items():
            for numero_semaines_range in numero_semaines_list:

                if len(numero_semaines_range) == 1:
                    numero_semaine = numero_semaines_range[0]
                    semaines_acceuil[numero_semaine] = self._make_semaine_acceuil(semaine_id)
                elif len(numero_semaines_range) == 2:
                    for numero_semaine in range(numero_semaines_range[0], numero_semaines_range[1]+1):
                        semaines_acceuil[numero_semaine] = self._make_semaine_acceuil(semaine_id)
                else:
                    raise ValueError(f"Invalid range: {numero_semaines_range}")

        return semaines_acceuil

    def _make_semaine_acceuil(self, semaine_id: int) -> SemaineAcceuil:
        """Make semaine acceuil"""
        semaine_type_data = self._data_loader.get_semaine_type_data(semaine_id)

        return SemaineAcceuil(
            lundi=self._make_jour_acceuil(semaine_type_data["lundi"]),
            mardi=self._make_jour_acceuil(semaine_type_data["mardi"]),
            mercredi=self._make_jour_acceuil(semaine_type_data["mercredi"]),
            jeudi=self._make_jour_acceuil(semaine_type_data["jeudi"]),
            vendredi=self._make_jour_acceuil(semaine_type_data["vendredi"]),
            samedi=self._make_jour_acceuil(semaine_type_data["samedi"]),
            dimanche=self._make_jour_acceuil(semaine_type_data["dimanche"]),
        )

    def _make_jour_acceuil(self, jour_id: int) -> JourAcceuil:
        """Make jour acceuil"""
        jour_type_data = self._data_loader.get_jour_type_data(jour_id)
        if not jour_type_data:
            return None

        creneau_horaire_data = jour_type_data[0]
        return JourAcceuil(creneau_horaire=self._make_creneau_horaire(creneau_horaire_data))

    def _make_creneau_horaire(self, creneau_horaire_data: list[str]) -> CreneauHoraire:
        """Make creneau horaire"""
        return CreneauHoraire(
            horaire_debut=time.fromisoformat(creneau_horaire_data[0] + ':00'),
            horaire_fin=time.fromisoformat(creneau_horaire_data[1] + ':00'))


def make_planning_with_range(semaines_acceuil_ranges: dict[tuple, SemaineAcceuil], semaines_conges_payes: list[int]):
    """Make Planning avec des intervals de semaines d acceuil"""
    semaines_acceuil = {}
    for intervals, semaine_acceuil in semaines_acceuil_ranges.items():
        for semaine in range(intervals[0], intervals[1]+1):
            semaines_acceuil[semaine] = deepcopy(semaine_acceuil)
    return Planning(semaines_acceuil, semaines_conges_payes)
