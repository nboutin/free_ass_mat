"""
:author Nicolas Boutin
:date 2023-07-05
"""
# pylint: disable=logging-fstring-interpolation

import logging
import calendar
from datetime import date, datetime

from controller.schedule import Schedule

logger = logging.getLogger(__name__)


class Garde:
    """Informations de garde réalisée, heure, gouter, repas, ..."""

    garde_info_t = dict[str, dict[str, str]]

    def __init__(self, garde_info: garde_info_t, schedule: Schedule) -> None:
        self._garde_info = garde_info
        self._schedule = schedule

    def get_heure_complementaire_du_mois(self, in_date: date) -> float:
        """
        :brief Calculate the number of complementary hours for a given month
        """
        # Get the number of days in the month
        _, num_days = calendar.monthrange(in_date.year, in_date.month)
        # Create a list of all days in the month
        dates = [date(in_date.year, in_date.month, day)
                 for day in range(1, num_days+1)]

        h_comp: float = 0.0
        for date_ in dates:
            h_trav_prevu = self._schedule.get_nb_heure_travaillee_par_jour(
                date_)
            date_str = date_.strftime('%Y-%m-%d')
            if date_str in self._garde_info:
                time_range = self._garde_info[date_str]
                start = datetime.strptime(time_range['start'], '%H:%M')
                end = datetime.strptime(time_range['end'], '%H:%M')
                h_trav_realisee: float = (end - start).seconds / 3600.0
                h_comp += max(h_trav_realisee - h_trav_prevu, 0.0)

        return h_comp

    def get_heure_majoree_du_mois(self, month: int) -> int:
        """
        :brief Calculate the number of additional hours for a given month
        """
        return 0
