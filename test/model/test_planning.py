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

from simple_ass_mat.model.planning import SemaineAcceuil    # nopep8 # noqa: E402
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


if __name__ == '__main__':
    import logging
    from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')])

    unittest.main()
