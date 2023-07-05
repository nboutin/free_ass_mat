"""
:author Nicolas Boutin
:date 2023-07-05
"""
# pylint: disable=logging-fstring-interpolation

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Schedule:
    """
    Schedule / planning, hour, day, week, month, year
    """
    week_range_t = list[dict[str, int]]

    day_id_t = int
    days_t = dict[day_id_t, dict[str, str]]

    week_id_t = int
    week_day_t = str  # monday, tuesday, wednesday, thursday, friday, saturday, sunday
    weeks_t = dict[week_id_t, dict[week_day_t, day_id_t]]

    def __init__(self, year: week_range_t, weeks: weeks_t, days: days_t, paid_vacation: week_range_t):
        self._year = year
        self._weeks = weeks
        self._days = days
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

    def get_working_hour_per_week(self, week_id: int = 0) -> float:
        """Calculate working hour per week"""
        hour_count = 0
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day_id = self._weeks[week_id][day]
            hour_count += self.get_working_hour_per_day(day_id)

        logger.debug(f"working hour per week = {hour_count}")
        return hour_count

    def get_working_hour_per_day(self, day_id: int) -> float:
        """Calculate working hour per day"""
        hour_count: float = 0.0
        if day_id is None:
            return hour_count

        for id_, time_ in self._days.items():
            if id_ == day_id:
                start = datetime.strptime(time_['start'], '%H:%M')
                end = datetime.strptime(time_['end'], '%H:%M')
                hour_count: float = (end - start).seconds / 3600.0

        logger.debug(f"working hour per day = {hour_count}")
        return hour_count

    def get_working_hour_per_month(self, week, days):
        """
        :brief Calculate working hour per month
        """
        return self.get_working_hour_per_week(week, days) * 52 / 12
