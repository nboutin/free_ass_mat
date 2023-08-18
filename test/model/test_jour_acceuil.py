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

from simple_ass_mat.model.planning import JourAcceuil, CreneauHoraire   # nopep8 # noqa: E402


class TestGetNombreHeureAcceuil(unittest.TestCase):

    def test_1_creneau_horaire(self):
        debut = time.fromisoformat('08:00:00')
        fin = time.fromisoformat('17:00:00')
        creneau = CreneauHoraire(debut, fin)
        jour = JourAcceuil(creneau)
        self.assertEqual(jour.get_nombre_heure_acceuil(), 9)


if __name__ == '__main__':
    import logging
    # from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')
        ])

    unittest.main()
