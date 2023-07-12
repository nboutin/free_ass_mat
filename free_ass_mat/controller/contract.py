"""
:author Nicolas Boutin
:date 2023-07-04
"""
# pylint: disable=logging-fstring-interpolation

import logging
import datetime
from typing import NamedTuple

from controller.schedule import Schedule
from controller.garde import Garde

logger = logging.getLogger(__name__)


class Contract:
    """Assistante maternelle contract"""

    class SalairesHoraires(NamedTuple):
        """Salaires namedtuple"""
        horaire_net: float
        horaire_complementaires: float
        horaire_majorees: float

    def __init__(self, schedule: Schedule, salaires: SalairesHoraires, garde: Garde) -> None:
        self._schedule = schedule
        self._salaires = salaires
        self._garde = garde

    @property
    def schedule(self) -> Schedule:
        """Schedule getter"""
        return self._schedule

    @property
    def garde(self) -> Garde:
        """Garde getter"""
        return self._garde

    @property
    def salaires_horaires(self) -> SalairesHoraires:
        """SalairesHoraires getter"""
        return self._salaires

    def get_salaire_net_mensualise(self):
        """working_hour_per_month_count * net_hourly_rate"""
        return self._schedule.get_heure_travaille_mois_mensualisee() * self._salaires.horaire_net

    def get_salaire_net_mois(self, date: datetime.date) -> float:
        """Salaire net mensuel incluant heure complementaire et heure majoree"""
        salaire_net_mensualise = self.get_salaire_net_mensualise()
        heure_absence_non_remuneree = self._garde.get_heure_absence_non_remuneree_mois(date)
        heure_travaille_prevu = self._schedule.get_heure_travaille_prevu_mois_par_date(date)

        return salaire_net_mensualise \
            - (salaire_net_mensualise * heure_absence_non_remuneree / heure_travaille_prevu) \
            + self._garde.get_heure_complementaire_mois(date) * self._salaires.horaire_complementaires \
            + self._garde.get_heure_majoree_mois(date) * self._salaires.horaire_majorees
