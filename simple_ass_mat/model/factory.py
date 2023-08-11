"""
Author: Nicolas Boutin
Date: 2023-08
Description:
"""

from copy import deepcopy
# from .contrat import Contrat
from .remuneration import Remuneration
from .planning import Planning, SemaineAcceuil


# def make_contrat(contrat_data) -> Contrat:
#     """Make Contrat"""
#     return Contrat(remuneration=make_remuneration(contrat_data["remuneration"]))


def make_remuneration(remuneration_data) -> Remuneration:
    """Make Remuneration"""
    return Remuneration(tarif_horaire_brut=remuneration_data["tarif_horaire_brut"])


def make_planning_with_range(semaines_acceuil_ranges: dict[tuple, SemaineAcceuil], semaines_conges_payes: list[int]):
    """Make Planning avec des intervals de semaines d acceuil
    """
    semaines_acceuil = {}
    for intervals, semaine_acceuil in semaines_acceuil_ranges.items():
        for semaine in range(intervals[0], intervals[1]+1):
            semaines_acceuil[semaine] = deepcopy(semaine_acceuil)
    return Planning(semaines_acceuil, semaines_conges_payes)
