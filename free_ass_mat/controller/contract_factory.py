"""
:author Nicolas Boutin
:date 2023-07-05
"""

from controller.schedule import Schedule
from controller.contract import Contract


def make_schedule(schedule_data):
    """
    :brief Construct schedule instance from schedule data read from file
    """
    return Schedule(schedule_data['year'], schedule_data['weeks'], schedule_data['days'], schedule_data['paid_vacation'])


def make_contract(contract_data):
    """
    :brief Construct contract instance from contract data read from file
    """
    schedule = make_schedule(contract_data['schedule'])
    return Contract(schedule)
