"""
:author Nicolas Boutin
:date 2023-07-05
"""

from .planning import Planning
from .planning_jour import PlanningJour
from .planning_semaine import PlanningSemaine
from .contrat import Contrat, IndemniteRepas
from .garde import Garde


def make_planning(planning_data):
    """
    :brief Construct planning instance from planning data read from file
    """
    planning_jour = PlanningJour(planning_data['jours'])
    planning_semaine = PlanningSemaine(planning_data['semaines'], planning_jour)
    return Planning(planning_jour, planning_semaine, planning_data['annee'], planning_data['conges_payes'])


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
    indemnite_repas = IndemniteRepas(
        dejeuner=contrat_data['indemnites_repas']['dejeuner'],
        gouter=contrat_data['indemnites_repas']['gouter'])
    return Contrat(planning, salaires, indemnite_repas, garde)
