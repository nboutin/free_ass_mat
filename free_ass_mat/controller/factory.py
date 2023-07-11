"""
:author Nicolas Boutin
:date 2023-07-05
"""

from controller.schedule import Schedule
from controller.contract import Contract
from controller.garde import Garde


def make_schedule(schedule_data):
    """
    :brief Construct schedule instance from schedule data read from file
    """
    return Schedule(schedule_data['year'], schedule_data['weeks'], schedule_data['days'],
                    schedule_data['paid_vacation'])


def make_garde_info(garde_info_data, schedule):
    """
    :brief Construct info_garde instance from info_garde data read from file
    """
    return Garde(garde_info_data, schedule)


def make_contract(contract_data):
    """
    :brief Construct contract instance from contract data read from file
    """
    schedule = make_schedule(contract_data['schedule'])
    garde = make_garde_info(contract_data['garde_info'], schedule)
    salaires_data = contract_data['salaires']
    salaires = Contract.SalairesHoraires(horaire_net=salaires_data['horaire_net'],
                                         horaire_complementaires=salaires_data['horaire_complementaires'],
                                         horaire_majorees=salaires_data['horaire_majorees'])
    return Contract(schedule, salaires, garde)
