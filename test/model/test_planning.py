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
from datetime import time


sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from simple_ass_mat.model.planning import CreneauHoraire, JourAcceuil, SemaineAcceuil    # nopep8 # noqa: E402
from simple_ass_mat.model.factory import make_planning_with_range  # nopep8 # noqa: E402


class TestConstructor(unittest.TestCase):

    def test_acceuil_first_then_conges(self):
        semaines_acceuil_intervals = {(1, 47): SemaineAcceuil()}
        conges_payes = [48, 49, 50, 51, 52]
        make_planning_with_range(semaines_acceuil_intervals, conges_payes)

    def test_split_conges(self):
        semaines_acceuil_intervals = {
            (1, 10): SemaineAcceuil(),
            (12, 20): SemaineAcceuil(),
            (22, 30): SemaineAcceuil(),
            (32, 40): SemaineAcceuil(),
            (42, 50): SemaineAcceuil(),
            (52, 52): SemaineAcceuil()}
        conges_payes = [11, 21, 31, 41, 51]
        make_planning_with_range(semaines_acceuil_intervals, conges_payes)


class TestGetNombreSemaineAcceuil(unittest.TestCase):

    def test_001(self):
        semaines_acceuil_intervals = {(1, 47): SemaineAcceuil()}
        conges_payes = [48, 49, 50, 51, 52]
        planning = make_planning_with_range(semaines_acceuil_intervals, conges_payes)
        self.assertEqual(planning.get_nombre_semaine_acceuil(), 47)


class TestGetNombreHeureSemaine(unittest.TestCase):

    def test_001(self):
        creneau = CreneauHoraire(time.fromisoformat('08:00:00'), time.fromisoformat('18:00:00'))
        jour = JourAcceuil(creneau)
        semaine_acceuil = SemaineAcceuil(lundi=jour, mardi=jour, jeudi=jour, vendredi=jour)
        semaines_acceuil_intervals = {(1, 47): semaine_acceuil}
        conges_payes = [48, 49, 50, 51, 52]
        planning = make_planning_with_range(semaines_acceuil_intervals, conges_payes)
        self.assertEqual(planning.get_nombre_heure_semaine(), 4*10)


if __name__ == '__main__':
    import logging
    # from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')
        ])

    unittest.main()
