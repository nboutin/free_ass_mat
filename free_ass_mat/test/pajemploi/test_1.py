"""
:date 2023-07-10
:author Nicolas Boutin
"""

# pylint: disable=logging-fstring-interpolation
# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import unittest
import sys
import os
import locale
from datetime import date
from pathlib import Path

import yaml


sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))  # OK


import controller.factory as factory  # nopep8 # noqa: E402


class TestPajemploi1(unittest.TestCase):
    """Test Pajemploi"""

    def setUp(self):
        locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')  # Set the French locale

        data_filepath = Path(__file__).parent / "data_1.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contract = factory.make_contract(data['contract'])
        self.schedule = self.contract.schedule
        self.garde = self.contract.garde

    def test_is_complete_year(self):
        self.assertTrue(self.contract.is_complete_year())

    def test_working_hour_per_week(self):
        self.assertEqual(self.schedule.get_heure_travaillee_semaine_par_id(), 32)

    def test_working_week_count(self):
        self.assertEqual(self.schedule.get_semaine_travaillee_annee(), 47)

    def test_working_hour_per_month(self):
        self.assertAlmostEqual(
            self.schedule.get_heure_travaille_mois_mensualisee(), 138.66, delta=0.01)

    def test_monthly_salary(self):
        self.assertEqual(self.contract.get_salaire_net_mensualise(), 416)

    def test_working_hour_per_month_normalized(self):
        self.assertEqual(
            self.schedule.get_heure_travaille_mois_mensualisee_normalisee(), 139)

    def test_working_day_per_month(self):
        self.assertAlmostEqual(self.schedule.get_jour_travaille_mois_mensualisee(), 17.33, delta=0.01)

    def test_working_day_per_month_normalized(self):
        self.assertEqual(
            self.schedule.get_jour_travaille_mois_mensualisee_normalise(), 18)

    def test_heure_complementaire_semaine(self):
        self.assertEqual(self.garde.get_heure_complementaire_semaine(2023, 2), 13)

    def test_heure_complementaire_mois(self):
        self.assertEqual(self.garde.get_heure_complementaire_mois(date(2023, 1, 1)), 13)

    def test_heure_majoree_semaine(self):
        self.assertEqual(self.garde.get_heure_majoree_semaine(2023, 2), 5)

    def test_heure_majorees_du_mois(self):
        self.assertEqual(self.garde.get_heure_majoree_mois(date(2023, 1, 1)), 5)

    def test_salaire_net_mois(self):
        self.assertEqual(self.contract.get_salaire_net_mois(date(2023, 1, 1)), 475.10)

    def test_jour_absence_non_remuneree_mois(self):
        self.assertEqual(self.garde.get_jour_absence_non_remuneree_mois(date(2023, 9, 1)), 8)

    def test_heure_absence_non_remuneree_mois(self):
        self.assertEqual(self.garde.get_heure_absence_non_remuneree_mois(date(2023, 9, 1)), 64)

    def test_jour_travaille_prevu_mois(self):
        self.assertEqual(self.schedule.get_jour_travaille_prevu_mois_par_date(date(2023, 9, 1)), 17)

    def test_heure_travaillee_prevu_mois(self):
        self.assertEqual(self.schedule.get_heure_travaille_prevu_mois_par_date(date(2023, 9, 1)), 136)

    def test_salaire_net_mois_2(self):
        self.assertAlmostEqual(self.contract.get_salaire_net_mois(date(2023, 9, 1)), 220.24, delta=0.01)


if __name__ == '__main__':
    unittest.main()
