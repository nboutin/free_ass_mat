"""
:author Nicolas Boutin
:date 2023-07-04
"""
# pylint: disable=logging-fstring-interpolation

import logging
from typing import NamedTuple

from controller.schedule import Schedule
from controller.garde import Garde

logger = logging.getLogger(__name__)


class Contract:
    """Assistante maternelle contract"""

    _COMPLETE_YEAR_WORKING_WEEK_COUNT = 47
    _COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT = 5

    class Salaires(NamedTuple):
        """Salaires namedtuple"""
        horaire_net: float
        horaire_complementaires: float
        horaire_majorees: float

    def __init__(self, schedule: Schedule, salaires: Salaires, garde: Garde) -> None:
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

    def is_complete_year(self) -> bool:
        """Evaluate if contract is for a complete year (47 week) or an incomplete year"""
        return (self._schedule.get_working_week_count() == Contract._COMPLETE_YEAR_WORKING_WEEK_COUNT) and \
            (self._schedule.get_paid_vacation_week_count() ==
             Contract._COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT)

    def get_basic_monthly_salary(self):
        """working_hour_per_month_count * net_hourly_rate"""

        return self._schedule.get_working_hour_per_month() * self._salaires.horaire_net
