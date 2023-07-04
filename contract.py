"""
:author Nicolas Boutin
:date 2023-07-04
"""
# pylint: disable=logging-fstring-interpolation

import logging

logger = logging.getLogger(__name__)

class Contract:
    """
    :brief Assistante maternelle contract
    """
    _COMPLETE_YEAR_WORKING_WEEK_COUNT = 47
    _COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT = 5
    
    def __init__(self):
        pass

    def is_complete_year(self, year, paid_vacation):
        """
        :brief Evaluate if contract is for a complete year (47 week) or an incomplete year
        :param year year to evaluate
        """

        return (Contract._count_working_week(year) == Contract._COMPLETE_YEAR_WORKING_WEEK_COUNT) \
            and (Contract._count_paid_vacation_week(paid_vacation) == Contract._COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT)
    
    @staticmethod
    def _count_working_week(year):
        """
        :brief Count week at work
        """
        week_count = 0
        for week_range in year:
            start = week_range['start']
            end = week_range['end']
            week_count += end - start + 1
        
        logger.debug(f"working week count = {week_count}")
        return week_count
    
    @staticmethod
    def _count_paid_vacation_week(paid_vacation):
        """
        :brief Count week of paid vacation
        """
        week_count = 0
        for week_range in paid_vacation:
            start = week_range['start']
            end = week_range['end']
            week_count += end - start + 1
        
        logger.debug(f"paid vacation week count = {week_count}")
        return week_count