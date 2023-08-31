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


sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from simple_ass_mat.model.remuneration import Remuneration  # nopep8 # noqa: E402


class TestTarifHoraireNet(unittest.TestCase):

    def test_brut_4_10(self):
        """
        tarif horaire brut = 4.10€
        """
        remuneration = Remuneration(4.10)
        self.assertAlmostEqual(remuneration.get_salaire_horaire_net(), 3.2029, delta=0.0001)


if __name__ == '__main__':
    import logging
    # from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')
    ])

    unittest.main()
