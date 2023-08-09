"""
:author Nicolas Boutin
:date 2023-08
"""
# pylint: disable=logging-fstring-interpolation

import datetime

from .. import helper
from .planning_error import JourIdError, HorairesError


class PlanningJour:
    """Gère le planning de garde pour un jour
    jours:
        0:
            horaires: dict[str, str]
            dejeuner: bool
            gouter: bool
    """

    jour_id_t = int
    horaires_t = dict[str, str]
    jours_t = dict[jour_id_t, horaires_t]

    def __init__(self, jours_data: jours_t) -> None:
        self._jours = jours_data

    def get_heures_travaillees(self, jour_id: jour_id_t) -> float:
        """Calcul le nombre d'heures travaillées pour un jour donné par jour_id"""
        horaires = self._get_horaires(jour_id)
        duree: datetime.timedelta = helper.convert_time_ranges_to_duration(horaires)
        heures_travaillees: float = duree.seconds / 3600.0
        return heures_travaillees

    def avec_frais_repas_dejeuner(self, jour_id: jour_id_t) -> bool:
        """Verifie si le dejeuner est compris pour un jour donné par jour_id"""
        try:
            jour = self._get_jour(jour_id)
        except JourIdError:
            return False

        try:
            return jour['dejeuner']
        except KeyError:
            return False

    def avec_frais_repas_gouter(self, jour_id: jour_id_t) -> bool:
        """Verifie si le gouter est compris pour un jour donné par jour_id"""
        try:
            jour = self._get_jour(jour_id)
        except JourIdError:
            return False

        try:
            return jour['gouter']
        except KeyError:
            return False

    def _get_jour(self, jour_id: jour_id_t) -> dict:
        """Return un jour par id"""
        try:
            jour = self._jours[jour_id]
        except KeyError as key_error:
            raise JourIdError(f"jour_id {jour_id} not found") from key_error

        return jour

    def _get_horaires(self, day_id: jour_id_t) -> horaires_t:
        """Return les horaires pour un jour donné par jour_id"""
        jour = self._get_jour(day_id)
        try:
            horaires = jour['horaires']
        except KeyError as key_error:
            raise HorairesError(f"horaires not found for {day_id}") from key_error

        return horaires
