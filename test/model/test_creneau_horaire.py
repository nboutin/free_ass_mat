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

from simple_ass_mat.model.planning import CreneauHoraire    # nopep8 # noqa: E402


class TestDuree(unittest.TestCase):

    def test_0800_1700(self):
        debut = time.fromisoformat('08:00:00')
        fin = time.fromisoformat('17:00:00')
        creneau = CreneauHoraire(debut, fin)
        self.assertEqual(creneau.duree().total_seconds()/3600, 9)

    def test_0000_2359(self):
        debut = time.fromisoformat('00:00:00')
        fin = time.fromisoformat('23:59:00')
        creneau = CreneauHoraire(debut, fin)
        self.assertEqual(creneau.duree().total_seconds()/60, 24*60-1)

    def test_0000_0001(self):
        debut = time.fromisoformat('00:00:00')
        fin = time.fromisoformat('00:01:00')
        creneau = CreneauHoraire(debut, fin)
        self.assertEqual(creneau.duree().total_seconds()/60, 1)

    def test_seconds_not_supported(self):
        debut = time.fromisoformat('08:00:10')
        fin = time.fromisoformat('18:00:40')
        creneau = CreneauHoraire(debut, fin)
        self.assertEqual(creneau.duree().total_seconds()/3600, 10)


if __name__ == '__main__':
    import logging
    # from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')
        ])

    unittest.main()
