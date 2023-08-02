"""
:date 2023-07-12
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

import yaml


sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))  # OK


import controller.factory as factory  # nopep8 # noqa: E402
from controller.pajemploi_declaration import PajemploiDeclaration  # nopep8 # noqa: E402


class TestTopAssMatMensualisation(unittest.TestCase):
    """Test Top AssMat Mensualisation
    https://aide.top-assmat.com/article/42-la-mensualisation
    """

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_pajemploi_exemple_annee_incomplete.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contrat = factory.make_contrat(data['contrat'])
        self.planning = self.contrat.planning
        self.garde = self.contrat.garde

        self.pajemploi_declaration = PajemploiDeclaration(self.contrat)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')

    unittest.main()
