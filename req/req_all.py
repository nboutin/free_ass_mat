"""
:date 2023-07-18
:author Nicolas Boutin
"""
# pylint: disable=logging-fstring-interpolation
# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import unittest
# import sys
# import os
from pathlib import Path

import yaml


# sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))  # OK


import free_ass_mat.controller.factory as factory  # nopep8 # noqa: E402
from free_ass_mat.controller.pajemploi_declaration import PajemploiDeclaration  # nopep8 # noqa: E402


class Req_All(unittest.TestCase):
    """"""

    def setUp(self):
        # data_filepath = Path(__file__).parent / "data_devenir_assmat_annee_complete.yml"
        # with open(data_filepath, 'r', encoding='UTF-8') as file:
        #     data = yaml.safe_load(file)
        # self.contrat = factory.make_contrat(data['contrat'])
        # self.schedule = self.contrat.schedule
        # self.garde = self.contrat.garde

        # self.pajemploi_declaration = PajemploiDeclaration(self.contrat)

    def req_heures_complementaires_001(self):
        """
        Les heures complémentaires correspondent aux heures effectuées entre la durée de
        travail hebdomadaire fixée au contrat de travail et la durée légale (45 h).
        Si le nombre d’heures complémentaires effectuées par l’assistant maternel, à votre demande,
        excède ⅓ de la durée des heures complémentaires prévues au contrat de travail, pendant 16 semaines consécutives,
        alors les parties doivent se rencontrer afin d’échanger sur les modalités d’organisation du travail.
        Les heures complémentaires, peuvent donner lieu à une majoration de salaire, sur décision écrite des parties
        prévue dans le contrat de travail.
        """

    def req_heures_majorees_001(self):
        """
        Toutes les heures travailles au dela de 45h/sem
        Pour un contrat mensualisé a 50h/sem, les 5h/sem majorees ne sont pas inclus dans le
        """


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, 'fr-FR')

    unittest.main()
