"""
:author Nicolas Boutin
:date 2023-07-04
"""
# pylint: disable=logging-fstring-interpolation

import logging
from datetime import datetime

from schedule import Schedule

logger = logging.getLogger(__name__)


class Contract:
    """
    :brief Assistante maternelle contract
    """
    _COMPLETE_YEAR_WORKING_WEEK_COUNT = 47
    _COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT = 5

    def __init__(self, schedule: Schedule):
        self._schedule = schedule

    def is_complete_year(self):
        """
        :brief Evaluate if contract is for a complete year (47 week) or an incomplete year
        :param year year to evaluate
        """
        return (self._schedule.get_working_week_count() == Contract._COMPLETE_YEAR_WORKING_WEEK_COUNT) and \
            (self._schedule.get_paid_vacation_week_count() == Contract._COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT)

        # return (Contract._count_working_week(year) == Contract._COMPLETE_YEAR_WORKING_WEEK_COUNT) \
        #     and (Contract._count_paid_vacation_week(paid_vacation) == Contract._COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT)

    def get_basic_monthly_salary(self, year, paid_vacation, hourly_rate):
        pass

    def get_working_hour_per_month(self, week, days):
        """
        :brief Calculate working hour per month
        """
        return self.get_working_hour_per_week(week, days) * 52 / 12

    def get_working_hour_per_week(self, week, days):
        """
        :brief Calculate working hour per week
        :param week week to evaluate
        """
        hour_count = 0
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            hour_count += self.get_working_hour_per_day(week[day], days)

        logger.debug(f"working hour per week = {hour_count}")
        return hour_count

    def get_working_hour_per_day(self, day, days):
        """
        :brief Calculate working hour per day
        """
        hour_count: float = 0.0
        if day is None:
            return hour_count

        for d in days:
            if d['id'] == day:
                start = datetime.strptime(d['start'], '%H:%M')
                end = datetime.strptime(d['end'], '%H:%M')
                hour_count: float = (end - start).seconds / 3600.0

        logger.debug(f"working hour per day = {hour_count}")
        return hour_count
