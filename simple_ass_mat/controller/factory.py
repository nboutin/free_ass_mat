"""
:author Nicolas Boutin
:date 2023-07-05
"""

from .planning import Planning
from .contrat import Contrat
from .garde import Garde


def make_planning(planning_data):
    """
    :brief Construct planning instance from planning data read from file
    """
    return Planning(planning_data['annee'], planning_data['semaines'], planning_data['jours'],
                    planning_data['conges_payes'])


def make_garde_info(garde_info_data, planning):
    """
    :brief Construct info_garde instance from info_garde data read from file
    """
    return Garde(garde_info_data, planning)


def make_contrat(contrat_data):
    """
    :brief Construct contrat instance from contrat data read from file
    """
    planning = make_planning(contrat_data['planning'])
    garde = make_garde_info(contrat_data['garde'], planning)
    salaires_data = contrat_data['salaires']
    salaires = Contrat.SalairesHoraires(horaire_net=salaires_data['horaire_net'],
                                        horaire_complementaires_net=salaires_data['horaire_complementaires_net'],
                                        horaire_majorees_net=salaires_data['horaire_majorees_net'])
    return Contrat(planning, salaires, garde)
