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
    
    data_contract = data['ass_mat']['employers'][0]['children'][0]['contract']
    contract = Contract()
    complete_year = contract.is_complete_year(data_contract['schedule']['year'], data_contract['schedule']['paid_vacation'])
    logger.info(f"Complete year {complete_year}")

if __name__ == "__main__":
    main()