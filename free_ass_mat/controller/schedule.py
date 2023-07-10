"""
:author Nicolas Boutin
:date 2023-07-05
"""
# pylint: disable=logging-fstring-interpolation

import logging
import math
import datetime
import calendar

import controller.helper as helper

logger = logging.getLogger(__name__)


class ScheduleError (ValueError):
    """Schedule error"""


class Schedule:
    """
    Schedule / planning, hour, day, week, month, year
    """
    day_id_t = int
    hour_range_t = dict[str, str]
    days_t = dict[day_id_t, hour_range_t]

    week_id_t = int
    week_day_t = str  # lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche
    weeks_t = dict[week_id_t, dict[week_day_t, day_id_t]]

    week_range_t = list[dict[str, int]]
    year_t = dict[week_id_t, week_range_t]

    def __init__(self, year: year_t, weeks: weeks_t, days: days_t, paid_vacation: week_range_t):
        self._year = year
        self._weeks = weeks
        self._days = days
        self._paid_vacation = paid_vacation

        self._check_input_data()

    def get_semaine_travaillee_annee(self) -> int:
        """Count working week for a complete year"""
        week_count = 0
        for week_id in self._year.keys():
            week_count += self._get_semaine_travaille_par_id(week_id)
        return week_count

    def _get_semaine_travaille_par_id(self, week_id: week_id_t) -> int:
        """Count working week for a given week_id"""
        week_count: int = 0
        for week_range in self._year[week_id]:
            start = week_range['start']
            end = week_range['end']
            week_count += end - start + 1
        return week_count

    def get_semaine_conges_payes_annee(self) -> int:
        """Count week of paid vacation"""
        week_count = 0
        for week_range in self._paid_vacation:
            start = week_range['start']
            end = week_range['end']
            week_count += end - start + 1
        return week_count

    def get_heure_travaille_semaine_par_date(self, year,  week_number: int) -> float:
        """Calculate working hour per week"""
        dates = helper.get_dates_in_week(year, week_number)
        week_id = self.get_semaine_id_par_date(dates[0])
        return self.get_heure_travaillee_semaine_par_id(week_id)

    def get_heure_travaillee_semaine_par_id(self, week_id: int = 0) -> float:
        """Calculate working hour per week"""
        hour_count = 0
        for day in calendar.day_name:
            day_id = self._weeks[week_id][day]
            hour_count += self.get_heure_travaillee_jour_par_id(day_id)
        return hour_count

    def get_heure_travaille_jour_par_date(self, date: datetime.date) -> float:
        """Calculate working hour per day"""
        day_id = self._get_jour_id_par_date(date)
        return self.get_heure_travaillee_jour_par_id(day_id)

    def get_heure_travaillee_jour_par_id(self, day_id: int) -> float:
        """Calculate working hour per day"""
        hour_count: float = 0.0
        if day_id is None:
            return hour_count

        for id_, time_range in self._days.items():
            if id_ == day_id:
                duration = helper.convert_time_range_to_duration(time_range)
                hour_count = duration.seconds / 3600.0

        logger.debug(f"working hour per day = {hour_count}")
        return hour_count

    def get_heure_travaille_mois_mensualisee(self) -> float:
        """Calculate working hour per month"""
        hour_per_week_count: float = 0.0
        for week_id in self._year.keys():
            # working_week_count = self._get_working_week_count(week_id)
            hour_per_week_count += self.get_heure_travaillee_semaine_par_id(week_id) * 52

        return hour_per_week_count / 12

    def get_heure_travaille_mois_mensualisee_normalisee(self) -> int:
        """<0.5, round down, >0.5, round up"""
        return round(self.get_heure_travaille_mois_mensualisee())

    def get_jour_travaille_semaine_par_id(self, week_id: int = 0) -> float:
        """working day count per week"""
        working_day_count = 0
        for day_id in self._weeks[week_id].values():
            if day_id is not None:
                working_day_count += 1
        return working_day_count

    def get_jour_travaille_mois_mensualisee(self) -> float:
        """day_per_week_count * 52 / 12"""
        return self.get_jour_travaille_semaine_par_id() * 52 / 12

    def get_jour_travaille_mois_mensualisee_normalise(self) -> int:
        """always round up"""
        return math.ceil(self.get_jour_travaille_mois_mensualisee())

    def _get_jour_id_par_date(self, date: datetime.date):
        """Get day id from date"""
        week_id = self.get_semaine_id_par_date(date)
        weekday_string = date.strftime('%A').lower()
        day_id = self._weeks[week_id][weekday_string]
        return day_id

    def get_semaine_id_par_date(self, date: datetime.date):
        """Get week id from date"""
        week_number: int = int(date.strftime('%U'))
        for id_, week_ranges in self._year.items():
            for week_range in week_ranges:
                if week_range['start'] <= week_number <= week_range['end']:
                    return id_
        raise ScheduleError(f"week id not found for date {date}")

    def get_jour_travaille_prevu_mois_par_date(self, date: datetime.date) -> int:
        """Get working day count for a given month"""
        jour: int = 0
        dates = helper.get_dates_in_month(date)

        for i_date in dates:
            day_id = self._get_jour_id_par_date(i_date)
            if day_id is not None:
                jour += 1
        return jour

    def get_heure_travaille_prevu_mois_par_date(self, date: datetime.date) -> float:
        """Get working hour planned for a month by date"""
        hour_count: float = 0.0
        dates = helper.get_dates_in_month(date)

        for i_date in dates:
            day_id = self._get_jour_id_par_date(i_date)
            if day_id is not None:
                hour_count += self.get_heure_travaillee_jour_par_id(day_id)
        return hour_count

    def _check_input_data(self) -> None:
        """
        Check that:
        - total number of week(working and paid vacation) is less or equal to 52
        - total number of working week is less or equal to 47
        - total number of paid vacation week is less or equal to 5
        """

        working_week_count = self.get_semaine_travaillee_annee()
        paid_vacation_week_count = self.get_semaine_conges_payes_annee()

        if working_week_count + paid_vacation_week_count > 52:
            raise ScheduleError(
                "Total number of week(working and paid vacation) is more than 52")

        if working_week_count > 47:
            raise ScheduleError("Total number of working week is more than 47")

        if paid_vacation_week_count > 5:
            raise ScheduleError(
                "Total number of paid vacation week is more than 5")
