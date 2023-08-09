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


from simple_ass_mat.controller import factory  # nopep8 # noqa: E402
from simple_ass_mat.controller.pajemploi_declaration import PajemploiDeclaration  # nopep8 # noqa: E402


class TestDevenirAssmatAnneeComplete3(unittest.TestCase):
    """Test Devenir AssMat"""

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_devenir_assmat_annee_complete_3.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contrat = factory.make_contrat(data['contrat'])
        self.planning = self.contrat.planning
        self.garde = self.contrat.garde

        self.pajemploi_declaration = PajemploiDeclaration(self.contrat)

    def test_calcul_annee_complete(self):
        """52 semaines, année complète
        47 semaines travaillées
        16 semaines, 4j/sem, 10h/j, 40h/sem
        36 semaines, 5j/sem, 9h/j, 45h/sem
        Salaire horaire net 4€
        Salaire net mensualisé 752€
        """
        self.assertTrue(self.planning.is_annee_complete())
        self.assertEqual(self.planning.annees.get_semaines_travaillees_count(), 47)
        self.assertEqual(self.planning.semaines.get_jours_travailles(0), 4)
        self.assertEqual(self.planning.semaines.get_jours_travailles(1), 5)
        self.assertEqual(self.planning.semaines.get_heures_travaillees(0), 40)
        self.assertEqual(self.planning.semaines.get_heures_travaillees(1), 45)
        self.assertAlmostEqual(self.planning.get_heures_travaillees_mois_mensualisees(), 189.93, delta=0.01)
        self.assertAlmostEqual(self.contrat.get_salaire_net_mensualise(), 759.72, delta=0.01)
        self.assertAlmostEqual(self.planning.get_jours_travailles_mois_mensualise(), 39.0, delta=0.01)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, 'fr-FR')

    unittest.main()
