"""
:date 2023-07-14
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


from controller import factory  # nopep8 # noqa: E402
from controller.pajemploi_declaration import PajemploiDeclaration  # nopep8 # noqa: E402


class TestDevenirAssmatAnneeIncomplete1(unittest.TestCase):
    """Test Devenir AssMat"""

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_devenir_assmat_annee_incomplete_1.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contrat = factory.make_contrat(data['contrat'])
        self.planning = self.contrat.planning
        self.garde = self.contrat.garde

        self.pajemploi_declaration = PajemploiDeclaration(self.contrat)

    def test_calcul_annee_complete(self):
        """
        4j/sem, 10h/j, 40h/sem, 6 semaines
        5j/sem, 9h/j, 45h/sem, 36 semaines
        Salaire horaire net 4€
        Salaire net mensualisé 620€
        """
        self.assertFalse(self.planning.is_annee_complete())
        self.assertEqual(self.planning.get_semaines_travaillees_annee(), 6+36)
        self.assertEqual(self.planning.get_jours_travailles_semaine_par_id(0), 4)
        self.assertEqual(self.planning.get_jours_travailles_semaine_par_id(1), 5)
        self.assertEqual(self.planning.get_heures_travaillees_semaine_par_id(0), 40)
        self.assertEqual(self.planning.get_heures_travaillees_semaine_par_id(1), 45)
        self.assertAlmostEqual(self.planning.get_heures_travaillees_mois_mensualisees(), 155, delta=0.01)
        self.assertAlmostEqual(self.contrat.get_salaire_net_mensualise(), 620, delta=0.01)
        self.assertAlmostEqual(self.planning.get_jours_travailles_mois_mensualise(), 17, delta=0.01)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, 'fr-FR')

    unittest.main()
