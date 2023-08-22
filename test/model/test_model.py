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

# from simple_ass_mat.model.planning import CreneauHoraire, JourAcceuil, SemaineAcceuil    # nopep8 # noqa: E402
# from simple_ass_mat.model.factory import make_planning_with_range  # nopep8 # noqa: E402
# from simple_ass_mat.model.contrat import Contrat  # nopep8 # noqa: E402
# from simple_ass_mat.model.remuneration import Remuneration  # nopep8 # noqa: E402


class TestLoadUserfile(unittest.TestCase):

    def test_001(self):
        """
        user file contains:
        1 contrat

        """



if __name__ == '__main__':
    import logging
    # from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')
    ])

    unittest.main()
