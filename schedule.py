"""
:author Nicolas Boutin
:date 2023-07-05
"""
# pylint: disable=logging-fstring-interpolation

import logging

logger = logging.getLogger(__name__)


class Schedule:
    """
    Schedule / planning, hour, day, week, month, year
    """
    week_range_t = list[dict[str, int]]

    def __init__(self, year: week_range_t, paid_vacation: week_range_t):
        self._year = year
        self._paid_vacation = paid_vacation

    def get_working_week_count(self) -> int:
        """
        :brief Count week at work
        """
        week_count = 0
        for week_range in self._year:
            start = week_range['start']
            end = week_range['end']
            week_count += end - start + 1

        logger.debug(f"working week count = {week_count}")
        return week_count

    def get_paid_vacation_week_count(self) -> int:
        """
        :brief Count week of paid vacation
        """
        week_count = 0
        for week_range in self._paid_vacation:
            start = week_range['start']
            end = week_range['end']
            week_count += end - start + 1

        logger.debug(f"paid vacation week count = {week_count}")
        return week_count
