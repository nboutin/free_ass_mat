"""
:author Nicolas Boutin
:date 2023-07-05
"""
# pylint: disable=logging-fstring-interpolation

import logging
import datetime
import calendar

import controller.helper as helper

logger = logging.getLogger(__name__)


class PlanningError (ValueError):
    """Planning error"""


class Planning:
    """
    Planning / planning, hour, day, week, month, year
    """
    _COMPLETE_YEAR_WORKING_WEEK_COUNT = 47
    _COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT = 5

    day_id_t = int
    hour_range_t = dict[str, str]
    days_t = dict[day_id_t, hour_range_t]

    week_id_t = int
    week_day_t = str  # lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche
    weeks_t = dict[week_id_t, dict[week_day_t, day_id_t]]

    week_range_t = list[dict[str, int]]
    year_t = dict[week_id_t, week_range_t]

    def __init__(self, annee: year_t, semaines: weeks_t, jours: days_t, conges_payes: week_range_t):
        self._year = annee
        self._weeks = semaines
        self._days = jours
        self._conges_payes = conges_payes

        self._check_input_data()

    def is_annee_complete(self) -> bool:
        """Evaluate if contrat is for a complete year (47 week) or an incomplete year"""
        return (self.get_semaines_travaillees_annee() == Planning._COMPLETE_YEAR_WORKING_WEEK_COUNT) and \
            (self.get_semaines_conges_payes_annee() == Planning._COMPLETE_YEAR_PAID_VACATION_WEEK_COUNT)

    def get_semaines_travaillees_annee(self) -> int:
        """Count working week for a complete year"""
        week_count = 0
        for week_id in self._year.keys():
            week_count += self._get_semaines_travaillees_par_id(week_id)
        return week_count

    def _get_semaines_travaillees_par_id(self, week_id: week_id_t) -> int:
        """Compte nombre de semaine travaille pour week_id donné"""
        week_count: int = 0
        for week_ranges in self._year[week_id]:
            if len(week_ranges) == 1:
                week_count += 1
            elif len(week_ranges) == 2:
                week_count += week_ranges[1] - week_ranges[0] + 1
            else:
                raise PlanningError(f"week_range length is not 1 or 2 for id {week_id}")
        return week_count

    def get_semaines_conges_payes_annee(self) -> int:
        """Count week of paid vacation"""
        week_count = 0
        for week_ranges in self._conges_payes:
            if len(week_ranges) == 1:
                week_count += 1
            elif len(week_ranges) == 2:
                week_count += week_ranges[1] - week_ranges[0] + 1
            else:
                raise PlanningError("week_range length is not 1 or 2 for conges_payes")
        return week_count

    def get_heure_travaillees_semaine_par_date(self, year,  week_number: int) -> float:
        """Calculate working hour per week"""
        dates = helper.get_dates_in_week(year, week_number)
        week_id = self.get_semaine_id_par_date(dates[0])
        return self.get_heures_travaillees_semaine_par_id(week_id)

    def get_heures_travaillees_semaine_par_id(self, week_id: int = 0) -> float:
        """Calculate working hour per week"""
        hour_count = 0
        for day in calendar.day_name:
            day_id = self._weeks[week_id][day]
            hour_count += self.get_heures_travaillees_jour_par_id(day_id)
        return hour_count

    def get_heures_travaillees_jour_par_date(self, date: datetime.date) -> float:
        """Calculate working hour per day"""
        day_id = self._get_jour_id_par_date(date)
        return self.get_heures_travaillees_jour_par_id(day_id)

    def get_heures_travaillees_jour_par_id(self, day_id: int) -> float:
        """Calculate working hour per day"""
        hour_count: float = 0.0
        if day_id is None:
            return hour_count

        for id_, time_ranges in self._days.items():
            if id_ == day_id:
                duration = helper.convert_time_ranges_to_duration(time_ranges)
                hour_count = duration.seconds / 3600.0

        return hour_count

    def get_heures_travaillees_mois_mensualisees(self) -> float:
        """Calculate working hour per month"""
        heures_travaillees_annee: float = 0.0
        for week_id in self._year.keys():
            if self.is_annee_complete():
                heures_travaillees_semaine = self.get_heures_travaillees_semaine_par_id(week_id)
                semaines_travaillees_annee = self._get_semaines_travaillees_par_id(week_id)
                semaines_travaillees_annee = semaines_travaillees_annee * 52 / 47
                heures_travaillees_annee += heures_travaillees_semaine * semaines_travaillees_annee
            else:
                semaines_travaillees_annee = self._get_semaines_travaillees_par_id(week_id)
                heures_travaillees_annee += self.get_heures_travaillees_semaine_par_id(week_id) \
                    * semaines_travaillees_annee

        return heures_travaillees_annee / 12

    def get_jours_travailles_semaine_par_id(self, week_id: int = 0) -> float:
        """working day count per week"""
        working_day_count = 0
        for day_id in self._weeks[week_id].values():
            if day_id is not None:
                working_day_count += 1
        return working_day_count

    def get_jours_travailles_mois_mensualise(self) -> float:
        """day_per_week_count * 52 / 12"""
        if self.is_annee_complete():
            return self.get_jours_travailles_semaine_par_id() * 52 / 12
        else:
            semaine_travaille_annee = self.get_semaines_travaillees_annee()
            return self.get_jours_travailles_semaine_par_id() * semaine_travaille_annee / 12

    def _get_jour_id_par_date(self, date: datetime.date):
        """Get jour_id par date"""
        week_id = self.get_semaine_id_par_date(date)
        weekday_string = date.strftime('%A').lower()
        day_id = self._weeks[week_id][weekday_string]
        return day_id

    def get_semaine_id_par_date(self, date: datetime.date):
        """Get week id from date"""
        week_number: int = int(date.strftime('%U'))
        for id_, week_ranges in self._year.items():
            for week_range in week_ranges:
                if len(week_range) == 1 and week_range == week_number:
                    return id_
                elif len(week_range) == 2:
                    if week_range[0] <= week_number <= week_range[1]:
                        return id_
        raise PlanningError(f"week id not found for date {date}")

    def get_jours_travailles_planifies_mois_par_date(self, date: datetime.date) -> int:
        """Get working day count for a given month"""
        jour: int = 0
        dates = helper.get_dates_in_month(date)

        for i_date in dates:
            day_id = self._get_jour_id_par_date(i_date)
            if day_id is not None:
                jour += 1
        return jour

    def get_heures_travaillees_prevu_mois_par_date(self, date: datetime.date) -> float:
        """Get working hour planned for a month by date"""
        hour_count: float = 0.0
        dates = helper.get_dates_in_month(date)

        for i_date in dates:
            day_id = self._get_jour_id_par_date(i_date)
            if day_id is not None:
                hour_count += self.get_heures_travaillees_jour_par_id(day_id)
        return hour_count

    def _check_input_data(self) -> None:
        """
        Check that:
        - total number of week(working and paid vacation) is less or equal to 52
        - total number of working week is less or equal to 47
        - total number of paid vacation week is less or equal to 5
        """

        working_week_count = self.get_semaines_travaillees_annee()
        paid_vacation_week_count = self.get_semaines_conges_payes_annee()

        if working_week_count + paid_vacation_week_count > 52:
            raise PlanningError(
                "Total number of week(working and paid vacation) is more than 52"
                f" ({working_week_count + paid_vacation_week_count}))")

        if working_week_count > 47:
            raise PlanningError(f"Total number of working week is more than 47 ({working_week_count})")

        if paid_vacation_week_count < 5:
            raise PlanningError(
                f"Total number of paid vacation week is less than 5 ({paid_vacation_week_count})")
