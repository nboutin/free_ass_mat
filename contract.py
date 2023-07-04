"""
:author Nicolas Boutin
:date 2023-07-04
"""

import logging

logger = logging.getLogger(__name__)

class Contract:
    """
    :brief Assistante maternelle contract
    """
    _COMPLETE_YEAR_WEEK_COUNT = 47
    
    def __init__(self):
        pass

    def is_complete_year(self, year):
        """
        :brief Evaluate if contract is for a complete year (47 week) or an incomplete year
        :param year year to evaluate
        """
        week_count = 0
        for week_range in year:
            start = week_range['start']
            end = week_range['end']
            week_count += end - start + 1
        
        logger.debug(f"week count = {week_count}")
        return week_count == Contract._COMPLETE_YEAR_WEEK_COUNT