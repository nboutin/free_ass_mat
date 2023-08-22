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

from simple_ass_mat.model.planning import SemaineAcceuil, JourAcceuil, CreneauHoraire   # nopep8 # noqa: E402


class TestGetNombreHeureAcceuil(unittest.TestCase):

    def test_001(self):
        """1 creneau horaire pour tous les jours de la semaines"""
        debut = time.fromisoformat('08:00:00')
        fin = time.fromisoformat('17:00:00')
        creneau = CreneauHoraire(debut, fin)
        jour = JourAcceuil(creneau)
        semaine = SemaineAcceuil(lundi=jour, mardi=jour, mercredi=jour, jeudi=jour,
                                 vendredi=jour, samedi=jour, dimanche=jour)
        self.assertEqual(semaine.get_nombre_heure_acceuil(), 9*7)

    def test_002(self):
        """1 creneau horaire different par jour"""
        lundi = JourAcceuil(CreneauHoraire(time.fromisoformat('12:00:00'),
                                           time.fromisoformat('13:00:00')))
        mardi = JourAcceuil(CreneauHoraire(time.fromisoformat('11:00:00'),
                                           time.fromisoformat('14:00:00')))
        mercredi = JourAcceuil(CreneauHoraire(time.fromisoformat('10:00:00'),
                                              time.fromisoformat('15:00:00')))
        jeudi = JourAcceuil(CreneauHoraire(time.fromisoformat('09:00:00'),
                                           time.fromisoformat('16:00:00')))
        vendredi = JourAcceuil(CreneauHoraire(time.fromisoformat('08:00:00'),
                                              time.fromisoformat('17:00:00')))
        samedi = JourAcceuil(CreneauHoraire(time.fromisoformat('07:00:00'),
                                            time.fromisoformat('18:00:00')))
        dimanche = JourAcceuil(CreneauHoraire(time.fromisoformat('06:00:00'),
                                              time.fromisoformat('19:00:00')))

        semaine = SemaineAcceuil(lundi=lundi, mardi=mardi, mercredi=mercredi, jeudi=jeudi,
                                 vendredi=vendredi, samedi=samedi, dimanche=dimanche)
        self.assertEqual(semaine.get_nombre_heure_acceuil(), 1+3+5+7+9+11+13)

    def test_003(self):
        """1 creneau horaire different par jour de la semaine,
        pas d'acceuil le weekend"""
        lundi = JourAcceuil(CreneauHoraire(time.fromisoformat('12:00:00'),
                                           time.fromisoformat('13:00:00')))
        mardi = JourAcceuil(CreneauHoraire(time.fromisoformat('11:00:00'),
                                           time.fromisoformat('14:00:00')))
        mercredi = JourAcceuil(CreneauHoraire(time.fromisoformat('10:00:00'),
                                              time.fromisoformat('15:00:00')))
        jeudi = JourAcceuil(CreneauHoraire(time.fromisoformat('09:00:00'),
                                           time.fromisoformat('16:00:00')))
        vendredi = JourAcceuil(CreneauHoraire(time.fromisoformat('08:00:00'),
                                              time.fromisoformat('17:00:00')))

        semaine = SemaineAcceuil(lundi=lundi, mardi=mardi, mercredi=mercredi, jeudi=jeudi,
                                 vendredi=vendredi)
        self.assertEqual(semaine.get_nombre_heure_acceuil(), 1+3+5+7+9)


if __name__ == '__main__':
    import logging
    # from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')
        ])

    unittest.main()
