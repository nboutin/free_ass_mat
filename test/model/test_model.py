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

from simple_ass_mat.model.model import Model  # nopep8 # noqa: E402
from simple_ass_mat.model.model_factory import ModelFactory  # nopep8 # noqa: E402
from simple_ass_mat.model.data_loader.data_loader_factory import DataLoaderFactory  # nopep8 # noqa: E402


class TestAddContrat(unittest.TestCase):

    def test_add_contrat(self):

        data_loader = DataLoaderFactory.make_data_loader("yaml")
        data_loader.load(Path(__file__).parent / "user_file" / "user_file_all_data.yml")
        model_factory = ModelFactory(data_loader)
        contrat = model_factory.make_contrat()

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
