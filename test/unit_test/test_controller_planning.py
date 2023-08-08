"""
:date 2023-08-07
:author Nicolas Boutin
"""

# pylint: disable=logging-fstring-interpolation
# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import unittest
import sys
import os
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))  # OK


from simple_ass_mat.controller.planning import Planning  # nopep8 # noqa: E402


class TestGetJourIdParDate(unittest.TestCase):

    def test_nominal(self):

        annee = {
            0: [[1, 5], [8, 14], [17, 27], [36, 42], [45, 51]],
            1: [[7], [16], [28], [34, 35], [44]]}

        semaines = {0: {"lundi": None, "mardi": None,
                        "mercredi": 1,
                        "jeudi": None,
                        "vendredi": None,
                        "samedi": None,
                        "dimanche": None},
                    1: {"lundi": None,
                        "mardi": 0,
                        "mercredi": 1,
                        "jeudi": 0,
                        "vendredi": 0,
                        "samedi": None,
                        "dimanche": None}}
        planning = Planning(annee, semaines, {}, [[1, 5]])

        self.assertEqual(planning.get_jour_id_par_date(date(2023, 1, 30)), None)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 1, 31)), None)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 1)), 1)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 2)), None)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 3)), None)

        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 6)), None)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 7)), None)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 8)), None)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 9)), None)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 10)), None)

        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 13)), None)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 14)), 0)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 15)), 1)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 16)), 0)
        self.assertEqual(planning.get_jour_id_par_date(date(2023, 2, 17)), 0)


class TestHeuresTravailleesJourParId(unittest.TestCase):

    def test_nominal(self):
        jours = {0: {"horaires": [["08:00", "18:00"]]}, 1: {"horaires": [["08:15", "18:30"]]}}
        planning = Planning({}, {}, jours, [[1, 5]])

        self.assertEqual(planning.get_heures_travaillees_jour_par_id(0), 10)
        self.assertEqual(planning.get_heures_travaillees_jour_par_id(1), 10.25)

    def test_two_hours_range_in_one_day(self):
        jours = {0: {"horaires": [["08:00", "12:00"], ["14:00", "18:00"]]}}
        planning = Planning({}, {}, jours, [[1, 5]])

        self.assertEqual(planning.get_heures_travaillees_jour_par_id(0), 8)

    def test_invalid_day_id(self):
        jours = {0: {"horaires": [["08:00", "18:00"]]}}
        planning = Planning({}, {}, jours, [[1, 5]])

        with self.assertRaises(ValueError):
            planning.get_heures_travaillees_jour_par_id(1)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, 'fr-FR')

    import logging
    from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')])

    unittest.main()
