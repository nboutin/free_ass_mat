"""
:author Nicolas Boutin
:date 2023-07-05
:details https://www.pajemploi.urssaf.fr/pajewebinfo/files/live/sites/pajewebinfo/files/contributed/pdf/employeur_ama/ExempleRemunerationAccueilRegulierAMA.pdf
"""
# pylint: disable=logging-fstring-interpolation
# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))  # OK

import unittest  # nopep8
from datetime import date  # nopep8
from pathlib import Path  # nopep8
import yaml  # nopep8

import controller.factory as factory  # nopep8


class TestPajemploi1(unittest.TestCase):

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_1.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contract = factory.make_contract(data['contract'])
        self.schedule = self.contract.schedule
        self.garde = self.contract.garde

    def test_working_hour_per_week(self):
        self.assertEqual(self.schedule.get_working_hour_per_week(), 32)

    def test_working_week_count(self):
        self.assertEqual(self.schedule.get_working_week_count(), 47)

    def test_working_hour_per_month(self):
        self.assertAlmostEqual(
            self.schedule.get_working_hour_per_month(), 138.66, delta=0.01)

    def test_monthly_salary(self):
        self.assertEqual(self.contract.get_basic_monthly_salary(), 416)

    def test_working_hour_per_month_normalized(self):
        self.assertEqual(
            self.schedule.get_working_hour_per_month_normalized(), 139)

    def test_working_day_per_month(self):
        self.assertAlmostEqual(self.schedule.get_working_day_per_month(), 17.33, delta=0.01)

    def test_working_day_per_month_normalized(self):
        self.assertEqual(
            self.schedule.get_working_day_per_month_normalized(), 18)
        
    def test_heure_complementaire_semaine(self):
        self.assertEqual(self.garde.get_heure_complementaire_semaine(2023, 2), 13)
        
    def test_heure_complementaire_mois(self):
        self.assertEqual(self.garde.get_heure_complementaire_mois(date(2023,1,1)), 13) 
        
    # def test_heure_majorees_du_mois(self):
    #     self.assertEqual(self.garde.get_heure_majoree_du_mois(date(2023,1,1)), 5)


if __name__ == '__main__':
    unittest.main()
