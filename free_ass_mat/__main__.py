"""
:author Nicolas Boutin
:date 2023-07-04
"""
# pylint: disable=logging-fstring-interpolation

import logging
import yaml

import controller.contract_factory as contract_factory

__NAME = "Free AssMat"

logger = logging.getLogger(__name__)


def main():
    """main"""
    logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Running {__NAME}")

    with open("data.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    for ass_mat in data['ass_mat']:
        logger.info(f"ass_mat first name: {ass_mat['first_name']}")
        logger.info(f"ass_mat surname: {ass_mat['surname']}")

        for employer in ass_mat['employers']:
            logger.info(f"employer first name: {employer['first_name']}")
            logger.info(f"employer surname: {employer['surname']}")

            for child in employer['children']:
                logger.info(f"child first name: {child['first_name']}")
                logger.info(f"child surname: {child['surname']}")

                contract = contract_factory.make_contract(child['contract'])
                schedule = contract.schedule

                complete_year = contract.is_complete_year()
                logger.info(f"Complete year {complete_year}")

                working_hour_per_week = schedule.get_working_hour_per_week()
                logger.info(f"working hour per week {working_hour_per_week}")

                working_hour_per_month = schedule.get_working_hour_per_month()
                logger.info(f"working hour per month {working_hour_per_month}")


if __name__ == "__main__":
    main()
