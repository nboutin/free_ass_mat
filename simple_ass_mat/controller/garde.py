"""
:author Nicolas Boutin
:date 2023-07-05
"""
# pylint: disable=logging-fstring-interpolation

import logging
import datetime

from . import helper
from .planning import Planning

logger = logging.getLogger(__name__)


class Garde:
    """Informations de garde réalisée, heure, gouter, repas, ..."""

    _HEURE_COMPLEMENTAIRE_SEUIL = 45

    garde_info_t = dict[str, dict[str, str]]

    def __init__(self, garde: garde_info_t, planning: Planning) -> None:
        self._garde = garde
        self._planning = planning

    def get_heures_travaillees_jour_par_date(self, date: datetime.date) -> float:
        """Nombre heures travaillees en un jour par date"""
        year_str = date.strftime('%Y')
        month_str = date.strftime('%m')
        day_str = date.strftime('%d')
        garde_day = None
        heures_travaillees_jour = 0.0

        try:
            garde_day = self._garde[year_str][month_str][day_str]
        except (KeyError, TypeError):
            # no information from garde data, use planning value
            heures_travaillees_jour = self._planning.get_heures_travaillees_jour_par_date(date)
        else:
            try:
                if garde_day['absence_payee']:
                    logger.debug(f"heures_travaillees_jour: {date} = {heures_travaillees_jour}")
                    return 0.0
            except KeyError:
                pass

            try:
                if garde_day['absence_non_remuneree']:
                    logger.debug(f"heures_travaillees_jour: {date} = {heures_travaillees_jour}")
                    return 0.0
            except KeyError:
                pass

            try:
                time_range = garde_day['heures']
                duration = helper.convert_time_ranges_to_duration(time_range)
                heures_travaillees_jour = duration.seconds / 3600.0
            except KeyError:
                pass

        logger.debug(f"heures_travaillees_jour: {date} = {heures_travaillees_jour}")
        return heures_travaillees_jour

    def get_heures_complementaires_jour_par_date(self, date: datetime.date) -> float:
        """Calculate the number of complementary hours for a given day
        Heure prévu - heure réalisée"""
        h_trav_prevu_jour = self._planning.get_heures_travaillees_jour_par_date(date)
        h_trav_realisee_jour = self.get_heures_travaillees_jour_par_date(date)
        return max(h_trav_realisee_jour - h_trav_prevu_jour, 0)  # cannot be negative

    def get_heures_complementaires_semaine_par_date(self, annee: int, numero_semaine: int) -> float:
        """Calculate the number of complementary hours for a given week"""
        h_comp_semaine: float = 0.0
        dates = helper.get_dates_in_week(annee, numero_semaine)

        for date_ in dates:
            h_comp_semaine += self.get_heures_complementaires_jour_par_date(date_)

        h_trav_prevu_semaine = self._planning. get_heure_travaillees_semaine_par_date(annee, numero_semaine)

        return max(
            min(h_trav_prevu_semaine + h_comp_semaine, Garde._HEURE_COMPLEMENTAIRE_SEUIL) - h_trav_prevu_semaine,
            0)

    def get_heures_complementaires_mois_par_date(self, date: datetime.date) -> float:
        """Calculate the number of complementary hours for a given month"""
        h_comp_mois: float = 0.0
        week_numbers = helper.get_week_numbers(date.year, date.month)

        for week_number in week_numbers:
            h_comp_mois += self.get_heures_complementaires_semaine_par_date(date.year, week_number)
        return h_comp_mois

    def has_heures_complementaires_mois(self, date: datetime.date) -> bool:
        """Check if there are complementary hours for a given month"""
        return self.get_heures_complementaires_mois_par_date(date) > 0.0

    def get_heures_majorees_semaine_par_date(self, annee: int, numero_semaine: int) -> float:
        """Calculate the number of additional hours for a given week"""
        h_comp_and_maj_semaine: float = 0.0
        dates = helper.get_dates_in_week(annee, numero_semaine)

        for date_ in dates:
            h_comp_and_maj_semaine += self.get_heures_complementaires_jour_par_date(date_)

        h_comp_semaine = self.get_heures_complementaires_semaine_par_date(annee, numero_semaine)

        return h_comp_and_maj_semaine - h_comp_semaine

    def get_heures_majorees_mois_par_date(self, date: datetime.date) -> float:
        """Calculate the number of additional hours for a given month"""
        h_maj_mois: float = 0.0
        week_numbers = helper.get_week_numbers(date.year, date.month)

        for week_number in week_numbers:
            h_maj_mois += self.get_heures_majorees_semaine_par_date(date.year, week_number)
        return h_maj_mois

    def has_jour_absence_non_remuneree_mois(self, date: datetime.date) -> bool:
        """Check if there are unpaid absence days for a given day"""
        return self.get_jour_absence_non_remuneree_mois(date) > 0

    def get_jour_absence_non_remuneree_mois(self, date: datetime.date) -> int:
        """Calculate the number of unpaid absence days for a given month"""
        jour_count: int = 0
        dates = helper.get_dates_in_month(date)

        for i_date in dates:
            year_str = i_date.strftime('%Y')
            month_str = i_date.strftime('%m')
            day_str = i_date.strftime('%d')
            try:
                if self._garde[year_str][month_str][day_str]['absence_non_remuneree']:
                    jour_count += 1
            except (KeyError, TypeError):
                pass

        return jour_count

    def get_heure_absence_non_remuneree_mois(self, date: datetime.date) -> float:
        """Calculate the number of unpaid absence hours for a given month"""
        heure_count: float = 0.0
        dates = helper.get_dates_in_month(date)

        for i_date in dates:
            year_str = i_date.strftime('%Y')
            month_str = i_date.strftime('%m')
            day_str = i_date.strftime('%d')
            try:
                if self._garde[year_str][month_str][day_str]['absence_non_remuneree']:
                    heure_count += self._planning.get_heures_travaillees_jour_par_date(i_date)
            except (KeyError, TypeError):
                pass

        return heure_count

    # def get_jour_travaillee_reel_mois(self, date: datetime.date) -> int:
    #     """Calculate the number of real working days for a given month"""
    #     pass
