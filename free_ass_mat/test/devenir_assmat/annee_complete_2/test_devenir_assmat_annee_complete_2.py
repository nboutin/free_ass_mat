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


class TestDevenirAssmatAnneeComplete2(unittest.TestCase):
    """Test Devenir AssMat"""

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_devenir_assmat_annee_complete_2.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contract = factory.make_contract(data['contract'])
        self.schedule = self.contract.schedule
        self.garde = self.contract.garde

        self.pajemploi_declaration = PajemploiDeclaration(self.contract)

    def test_calcul_annee_complete(self):
        """52 semaines, année complète
        47 semaines travaillées
        11 semaines, 4j/sem, 8h/j, 32h/sem
        36 semaines, 5j/sem, 8h/j, 40h/sem
        Salaire horaire net 3€
        Salaire net mensualisé 498€
        """
        self.assertTrue(self.schedule.is_annee_complete())
        self.assertEqual(self.schedule.get_semaines_travaillees_annee(), 47)
        self.assertEqual(self.schedule.get_jours_travailles_semaine_par_id(0), 5)
        self.assertEqual(self.schedule.get_jours_travailles_semaine_par_id(1), 4)
        self.assertEqual(self.schedule.get_heures_travaillees_semaine_par_id(0), 40)
        self.assertEqual(self.schedule.get_heures_travaillees_semaine_par_id(1), 32)
        self.assertAlmostEqual(self.schedule.get_heures_travaillees_mois_mensualisees(), 146.78, delta=0.01)
        self.assertAlmostEqual(self.contract.get_salaire_net_mensualise(), 440.34, delta=0.01)
        self.assertAlmostEqual(self.schedule.get_jours_travailles_mois_mensualise(), 21.66, delta=0.01)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')

    unittest.main()
