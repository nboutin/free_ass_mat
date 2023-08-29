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
from simple_ass_mat.model.model_factory import make_planning_with_range  # nopep8 # noqa: E402
from simple_ass_mat.model.contrat import Contrat  # nopep8 # noqa: E402
from simple_ass_mat.model.remuneration import Remuneration  # nopep8 # noqa: E402


class TestGetDureeAcceuilHebdomadaireMoyen(unittest.TestCase):

    def test_001(self):
        """
        47 semaines d'acceuil
        5 semaines de conges payes
        1 semaine de 5 jour de 8h
        """
        jour = JourAcceuil(CreneauHoraire(time.fromisoformat("08:00:00"), time.fromisoformat("16:00:00")))
        semaines_acceuil_intervals = {
            (1, 47): SemaineAcceuil(lundi=jour, mardi=jour, mercredi=jour, jeudi=jour, vendredi=jour)}
        conges_payes = [48, 49, 50, 51, 52]
        planning = make_planning_with_range(semaines_acceuil_intervals, conges_payes)
        remuneration = Remuneration(4.10)
        contrat = Contrat(planning, remuneration)
        self.assertEqual(contrat.get_duree_acceuil_hebdomadaire_moyen(), 47*8*5/52)


class TestGetDureeAccueilMensualisee(unittest.TestCase):

    def test_001(self):
        """
        47 semaines d'acceuil
        5 semaines de conges payes
        1 semaine de 5 jour de 8h
        """
        jour = JourAcceuil(CreneauHoraire(time.fromisoformat("08:00:00"), time.fromisoformat("16:00:00")))
        semaines_acceuil_intervals = {
            (1, 47): SemaineAcceuil(lundi=jour, mardi=jour, mercredi=jour, jeudi=jour, vendredi=jour)}
        conges_payes = [48, 49, 50, 51, 52]
        planning = make_planning_with_range(semaines_acceuil_intervals, conges_payes)
        remuneration = Remuneration(4.10)
        contrat = Contrat(planning, remuneration)
        self.assertEqual(contrat.get_duree_acceuil_mensualisee(), 8*5*52/12)


class TestGetRemunerationBrutMensualisee(unittest.TestCase):

    def test_001(self):
        """
        47 semaines d'acceuil
        5 semaines de conges payes
        1 semaine de 5 jour de 8h
        """
        jour = JourAcceuil(CreneauHoraire(time.fromisoformat("08:00:00"), time.fromisoformat("16:00:00")))
        semaines_acceuil_intervals = {
            (1, 47): SemaineAcceuil(lundi=jour, mardi=jour, mercredi=jour, jeudi=jour, vendredi=jour)}
        conges_payes = [48, 49, 50, 51, 52]
        planning = make_planning_with_range(semaines_acceuil_intervals, conges_payes)
        remuneration = Remuneration(4.10)
        contrat = Contrat(planning, remuneration)
        self.assertEqual(contrat.get_remuneration_brut_mensualisee(), 4.10*8*5*52/12)


if __name__ == '__main__':
    import logging
    # from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')
        ])

    unittest.main()
