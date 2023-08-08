"""
:author Nicolas Boutin
:date 2023-08
"""
# pylint: disable=logging-fstring-interpolation

from .planning_error import PlanningAnneeError, SemaineIdError


class PlanningAnnee:
    """Gere le planning de garde pour une année"""

    semaine_id_t = int
    week_range_t = list[dict[str, int]]
    year_t = dict[semaine_id_t, week_range_t]

    def __init__(self, annees_data: year_t) -> None:
        self._annees = annees_data

    @property
    def annee_ids(self) -> set[int]:
        """Return annee_ids"""
        return self._annees.keys()

    def get_semaines_travaillees_count(self) -> int:
        """Count working week for a complete year"""
        semaine_count = 0
        for semaine_id in self._annees.keys():
            semaine_count += self.get_semaines_travaillees_count_par_id(semaine_id)
        return semaine_count

    def get_semaines_travaillees_count_par_id(self, semaine_id: semaine_id_t) -> int:
        """Compte nombre de semaine travaille pour week_id donné"""
        semaine_count: int = 0
        for semaine_interval in self._annees[semaine_id]:
            if len(semaine_interval) == 1:
                semaine_count += 1
            elif len(semaine_interval) == 2:
                semaine_count += semaine_interval[1] - semaine_interval[0] + 1
            else:
                raise PlanningAnneeError(f"semaine_interval length is not 1 or 2 for semaine_id {semaine_id}")
        return semaine_count

    def get_semaine_id(self, semaine_numero: int) -> semaine_id_t:
        """Retourne l'id de la semaine pour le numéro de semaine donné"""
        for semaine_id, semaine_intervals in self._annees.items():
            for semaine_interval in semaine_intervals:
                if len(semaine_interval) == 1 and semaine_interval[0] == semaine_numero:
                    return semaine_id

                if len(semaine_interval) == 2:
                    if semaine_interval[0] <= semaine_numero <= semaine_interval[1]:
                        return semaine_id
        raise SemaineIdError(f"semaine_id not found for semaine_numero: {semaine_numero}")
