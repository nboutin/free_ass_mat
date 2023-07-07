"""
:author Nicolas Boutin
:date 2023-07-05
"""
# pylint: disable=logging-fstring-interpolation

import logging
from datetime import date

import controller.helper as helper
from controller.schedule import Schedule

logger = logging.getLogger(__name__)


class Garde:
    """Informations de garde réalisée, heure, gouter, repas, ..."""

    _HEURE_COMPLEMENTAIRE_SEUIL = 45

    garde_info_t = dict[str, dict[str, str]]

    def __init__(self, garde_info: garde_info_t, schedule: Schedule) -> None:
        self._garde_info = garde_info
        self._schedule = schedule
    
    def get_heure_travaille_par_jour(self, in_date) -> float:
        """Compute number of hour worked for a day"""
        date_str = in_date.strftime('%Y-%m-%d')
        if date_str not in self._garde_info:
            return 0.0
        
        time_range = self._garde_info[date_str]
        duration = helper.convert_time_range_to_duration(time_range)
        return duration.seconds / 3600.0
        
    def get_heure_complementaire_jour(self, in_date: date) -> float:
        """Calculate the number of complementary hours for a given day
        Heure prévu - heure réalisée"""
        h_trav_prevu_jour = self._schedule.get_nb_heure_travaillee_par_jour(in_date)
        h_trav_realisee_jour = self.get_heure_travaille_par_jour(in_date)
        return max(h_trav_realisee_jour - h_trav_prevu_jour, 0) # cannot be negative
        
    def get_heure_complementaire_semaine(self, year: int, numero_semaine:int)->float:
        """Calculate the number of complementary hours for a given week"""
        h_comp_semaine: float =  0.0
        dates = helper.get_dates_in_week(year, numero_semaine)
        
        for date_ in dates:
            h_comp_semaine += self.get_heure_complementaire_jour(date_)
            
        h_trav_prevu_semaine = self._schedule. get_working_hour_per_week_from_week_number(year, numero_semaine)
        
        return min(h_trav_prevu_semaine + h_comp_semaine, Garde._HEURE_COMPLEMENTAIRE_SEUIL) - h_trav_prevu_semaine

    # def get_heure_complementaire_du_mois(self, in_date: date) -> float:
    #     """Calculate the number of complementary hours for a given month"""
    #     # h_trav_prevu_semaine = self._schedule.get_working_hour_per_week()

    #     h_comp_mois: float = 0.0
    #     dates = helper.get_dates_in_month(in_date)

    #     for date_ in dates:
    #         h_comp_mois += self.get_heure_complementaire_jour(date_)

    #     return min(h_comp_mois, Garde._HEURE_COMPLEMENTAIRE_SEUIL)

        

    def get_heure_majoree_du_mois(self, in_date: date) -> float:
        """Calculate the number of additional hours for a given month"""
        return 0
