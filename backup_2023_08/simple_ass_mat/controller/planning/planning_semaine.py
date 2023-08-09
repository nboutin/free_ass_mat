"""
:author Nicolas Boutin
:date 2023-08
"""
# pylint: disable=logging-fstring-interpolation

import calendar

from .planning_jour import PlanningJour
from .planning_error import JourIdError, SemaineIdError


class PlanningSemaine:
    """Gère le planning de garde pour une semaine"""

    semaine_id_t = int
    jour_nom_t = str  # lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche
    semaines_t = dict[semaine_id_t, dict[jour_nom_t, PlanningJour.jour_id_t]]

    def __init__(self, semaines_data: semaines_t, jours: PlanningJour) -> None:
        self._semaines = semaines_data
        self._jours = jours

    @property
    def semaine_ids(self) -> set[semaine_id_t]:
        """Return semaine ids"""
        return self._semaines.keys()

    def get_heures_travaillees(self, semaine_id: semaine_id_t) -> float:
        """Calculate working hour per week"""
        heures_travaillees = 0

        for jour_nom in calendar.day_name:
            semaine = self._get_semaine(semaine_id)
            jour_id = semaine[jour_nom]
            try:
                heures_travaillees += self._jours.get_heures_travaillees(jour_id)
            except JourIdError:
                pass

        return heures_travaillees

    def get_jours_travailles(self, semaine_id: semaine_id_t) -> float:
        """Calcul le nombre de jour travaillé dans la semaine"""
        jours_travailles = 0
        for jour_id in self._semaines[semaine_id].values():
            if jour_id is not None:
                jours_travailles += 1
        return jours_travailles

    def get_jour_id(self, semaine_id: semaine_id_t, jour_nom: jour_nom_t) -> PlanningJour.jour_id_t:
        """Return jour id"""
        return self._get_semaine(semaine_id)[jour_nom]

    def _get_semaine(self, semaine_id: semaine_id_t):
        """Return semaine"""
        try:
            return self._semaines[semaine_id]
        except KeyError as key_error:
            raise SemaineIdError(f"semaines_id {semaine_id} not found") from key_error
