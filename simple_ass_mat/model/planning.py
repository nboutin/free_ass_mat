"""
Author: Nicolas Boutin
Date: 2023-08
Description: Represent le planning de garde prevu par le contrat
"""

from datetime import time, timedelta


class PlanningError(ValueError):
    """Planning error"""


class CreneauHoraire:
    """Creneau horaire"""

    def __init__(self, horaire_debut: time, horaire_fin: time) -> None:
        self._horaire_debut = horaire_debut
        self._horaire_fin = horaire_fin

    @property
    def duree(self) -> timedelta:
        """Return duree"""
        return timedelta(hours=self._horaire_fin.hour, minutes=self._horaire_fin.minute,) \
            - timedelta(hours=self._horaire_debut.hour, minutes=self._horaire_debut.minute)


class JourAcceuil:
    """Jour acceuil"""

    def __init__(self, creneau_horaire: CreneauHoraire | None = None) -> None:
        self._creneau_horaire = creneau_horaire


class SemaineAcceuil:
    """Semaine acceuil"""

    jour_t = JourAcceuil | None

    def __init__(self, lundi: jour_t = None, mardi: jour_t = None, mercredi: jour_t = None,
                 jeudi: jour_t = None, vendredi: jour_t = None, samedi: jour_t = None, dimanche: jour_t = None) -> None:
        self._jours = {"lundi": lundi, "mardi": mardi, "mercredi": mercredi,
                       "jeudi": jeudi, "vendredi": vendredi, "samedi": samedi, "dimanche": dimanche}


class Planning:
    """Planning de garde de l'enfant
    Pour chaque numero de semaine dans une annee, on definit:
    - soit une semaine acceuil
    - soit une semaine de conges payes ass_mat
    """

    _NOMBRE_SEMAINES_CONGES_PAYES = 5
    _NOMBRE_SEMAINES_ACCEUIL = 47

    def __init__(self, semaines_acceuil: dict[int, SemaineAcceuil], semaines_conges_payes: list[int]) -> None:
        """
        semaines_acceuil= dict[0:semaine, 10:semaine, ...]
        semaines_conges_payes= list[int]
        """
        self._check_inputs(semaines_acceuil, semaines_conges_payes)
        self._semaines_acceuil = semaines_acceuil
        self._semaines_conges_payes = semaines_conges_payes

    @staticmethod
    def _check_inputs(semaines_acceuil, semaines_conges_payes):
        """
        Verifier:
        - nombre de semaine de conges payes = 5
        - nombre de semaines acceuil = 47
        - les dates des conges payes sont differentes des dates d'acceuil
        """

        if len(semaines_conges_payes) != Planning._NOMBRE_SEMAINES_CONGES_PAYES:
            raise PlanningError(
                f"Nombre de semaines de conges payes different de {Planning._NOMBRE_SEMAINES_CONGES_PAYES}"
                f" égal {len(semaines_conges_payes)}")

        if len(semaines_acceuil) != Planning._NOMBRE_SEMAINES_ACCEUIL:
            raise PlanningError(
                f"Nombre de semaines d'acceuil different de {Planning._NOMBRE_SEMAINES_ACCEUIL}"
                f" égal {len(semaines_acceuil)}")

        for numero_semaine_cp in semaines_conges_payes:
            if numero_semaine_cp in semaines_acceuil.keys():
                raise PlanningError(
                    f"Semaine de conges payes {numero_semaine_cp} est aussi une semaine d'acceuil")
