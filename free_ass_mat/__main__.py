"""
:author Nicolas Boutin
:date 2023-07-04
"""
# pylint: disable=logging-fstring-interpolation

import logging
import yaml

from controller import factory

__NAME = "Free AssMat"

logger = logging.getLogger(__name__)


def main():
    """main"""
    logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Running {__NAME}")

    with open("data.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    for ass_mat in data['ass_mat']:
        logger.info(f"ass_mat first name: {ass_mat['prenom']}")
        logger.info(f"ass_mat nom: {ass_mat['nom']}")

        for employer in ass_mat['employers']:
            logger.info(f"employer first name: {employer['prenom']}")
            logger.info(f"employer nom: {employer['nom']}")

            for child in employer['children']:
                logger.info(f"child first name: {child['prenom']}")
                logger.info(f"child nom: {child['nom']}")

                contrat = factory.make_contrat(child['contrat'])
                planning = contrat.planning

                complete_year = contrat.is_annee_complete()
                logger.info(f"Complete year {complete_year}")

                working_hour_per_week = planning.get_heures_travaillees_semaine_par_id()
                logger.info(f"working hour per week {working_hour_per_week}")

                working_hour_per_month = planning.get_heures_travaillees_mois_mensualisees()
                logger.info(f"working hour per month {working_hour_per_month}")

                basic_monthly_salary = contrat.get_salaire_net_mensualise()
                logger.info(f"basic monthly salary {basic_monthly_salary}")


if __name__ == "__main__":
    main()
