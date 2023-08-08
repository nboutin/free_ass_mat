"""
:date 2023-08
:author Nicolas Boutin
"""

# pylint: disable=logging-fstring-interpolation
# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))  # OK


from simple_ass_mat.controller.planning_jour import PlanningJour, JourIdError  # nopep8 # noqa: E402


class TestHeuresTravailleesJourParId(unittest.TestCase):

    def test_nominal(self):
        jours = {0: {"horaires": [["08:00", "18:00"]]}, 1: {"horaires": [["08:15", "18:30"]]}}
        planning_jour = PlanningJour(jours)

        self.assertEqual(planning_jour.get_heures_travaillees(0), 10)
        self.assertEqual(planning_jour.get_heures_travaillees(1), 10.25)

    def test_two_hours_range_in_one_day(self):
        jours = {0: {"horaires": [["08:00", "12:00"], ["14:00", "18:00"]]}}
        planning_jour = PlanningJour(jours)

        self.assertEqual(planning_jour.get_heures_travaillees(0), 8)

    def test_invalid_day_id(self):
        jours = {0: {"horaires": [["08:00", "18:00"]]}}
        planning_jour = PlanningJour(jours)

        with self.assertRaises(JourIdError):
            planning_jour.get_heures_travaillees(1)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, 'fr-FR')

    import logging
    from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')])

    unittest.main()
