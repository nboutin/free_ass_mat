"""
:date 2023-08-03
:author Nicolas Boutin
"""

# pylint: disable=logging-fstring-interpolation
# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import unittest
import sys
import os
from datetime import date
from pathlib import Path

import yaml


sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))  # OK


import controller.factory as factory  # nopep8 # noqa: E402
from controller.pajemploi_declaration import PajemploiDeclaration  # nopep8 # noqa: E402


class TestParentUsecase1(unittest.TestCase):
    """Test parent usecase 1"""

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_parent_usecase_1b.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contrat = factory.make_contrat(data['contrat'])
        self.planning = self.contrat.planning
        self.garde = self.contrat.garde

        self.pajemploi_declaration = PajemploiDeclaration(self.contrat)

    def test_contrat_parametres(self):
        """année incomplète
        43 semaines travaillées
        Mardi,Jeudi,Vendredi 8h-17h45 et Mercredi 8h-16h30 37.75h/semaine
        Salaire net horaire 3.2029€
        Heure complémentaire 3.2029€
        Heure majorée 3.52€
        Nombre heure par mensualise = 135.27h
        Nombre de jours activités mensualises = 14.33j
        Declaration Pajemploi:
        - Nombre d'heures normales = 136
        - Nombre de jours d'activités = 15
        """
        self.assertFalse(self.planning.is_annee_complete())
        self.assertEqual(self.planning.get_semaines_travaillees_annee(), 43)
        self.assertEqual(self.planning.get_heures_travaillees_semaine_par_id(), 37.75)
        self.assertAlmostEqual(self.planning.get_heures_travaillees_mois_mensualisees(), 135.27, delta=0.01)
        self.assertAlmostEqual(self.contrat.get_salaire_net_mensualise(), 433.26, delta=0.01)
        self.assertAlmostEqual(self.planning.get_jours_travailles_mois_mensualise(), 14.33, delta=0.01)

    def test_mois_nominal(self):
        """Mois nominal
        frais d'entretien: 18j
        13j 9h45 = 13j * 4€
        5j 8h30 = 5j * 3.49€
        total = 69.45€
        """
        mois_courant = date(2022, 11, 1)
        today = date(2022, 12, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue
        remuneration = declaration.remuneration

        self.assertEqual(travail_effectue.nombre_heures_normales, 135)
        self.assertEqual(travail_effectue.nombre_jours_activite, 15)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertFalse(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 433.26, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 69.45, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertTrue(remuneration.avec_indemnite_repas_ou_kilometrique)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')

    unittest.main()
