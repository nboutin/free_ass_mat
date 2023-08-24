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
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

# # from simple_ass_mat.model.factory import make_planning_with_range  # nopep8 # noqa: E402
from simple_ass_mat.model.model import Model  # nopep8 # noqa: E402


class TestAddContrat(unittest.TestCase):

    def test_add_contrat(self):

        contrat = 

        model = Model()
        model.add_contrat(contrat)


if __name__ == '__main__':
    import logging
    # from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')
    ])

    unittest.main()
