"""
:author Nicolas Boutin
:date 2023-07-04
"""
# pylint: disable=logging-fstring-interpolation

import logging
import yaml

from contract import Contract

__NAME = "Free AssMat"

logger = logging.getLogger(__name__)

def main():
    """main"""
    logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Running {__NAME}")
    
    with open ("data.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # logger.info(f"Data: {data}")
    
    contract_data = data['ass_mat']['employers'][0]['children'][0]['contract']
    contract = Contract()
    schedule_data = contract_data['schedule']
    complete_year = contract.is_complete_year(schedule_data['year'], schedule_data['paid_vacation'])
    logger.info(f"Complete year {complete_year}")

    working_hour_per_week = contract.get_working_hour_per_week(schedule_data['weeks'][0], schedule_data['days'])
    logger.info(f"working hour per week {working_hour_per_week}")

if __name__ == "__main__":
    main()