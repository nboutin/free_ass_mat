"""
:date 2023-07-12
:author Nicolas Boutin
:brief https://devenirassmat.com/la-mensualisation-cest-obligatoire/
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


sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))  # OK


import controller.factory as factory  # nopep8 # noqa: E402
from controller.pajemploi_declaration import PajemploiDeclaration  # nopep8 # noqa: E402


class TestDevenirAssmatAnneeComplete(unittest.TestCase):
    """Test Devenir AssMat"""

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_devenir_assmat_annee_complete.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contrat = factory.make_contrat(data['contrat'])
        self.planning = self.contrat.planning
        self.garde = self.contrat.garde

        self.pajemploi_declaration = PajemploiDeclaration(self.contrat)

    def test_calcul_annee_complete(self):
        """52 semaines, année complète
        47 semaines travaillées
        5j/semaine, 40h/semaine
        Salaire horaire net 3€
        Salaire net mensualisé 520€
        """
        self.assertTrue(self.planning.is_annee_complete())
        self.assertEqual(self.planning.get_jours_travailles_semaine_par_id(), 5)
        self.assertEqual(self.planning.get_heures_travaillees_semaine_par_id(), 40)
        self.assertEqual(self.contrat.get_salaire_net_mensualise(), 520)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')

    unittest.main()
