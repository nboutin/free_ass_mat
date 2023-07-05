"""
:author Nicolas Boutin
:date 2023-07-04
"""
# pylint: disable=logging-fstring-interpolation

import logging

from schedule import Schedule

logger = logging.getLogger(__name__)


class Contract:
    """Assistante maternelle contract"""
    
    _COMPLETE_YEAR_WORKING_WEEK_COUNT = 47
    _COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT = 5

    def __init__(self, schedule: Schedule) -> None:
        self._schedule = schedule
        
    @property
    def schedule(self) -> Schedule:
        """Schedule getter"""
        return self._schedule

    def is_complete_year(self) -> bool:
        """Evaluate if contract is for a complete year (47 week) or an incomplete year"""
        return (self._schedule.get_working_week_count() == Contract._COMPLETE_YEAR_WORKING_WEEK_COUNT) and \
            (self._schedule.get_paid_vacation_week_count() ==
             Contract._COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT)

    def get_basic_monthly_salary(self, year, paid_vacation, hourly_rate):
        pass


