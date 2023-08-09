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
from pathlib import Path
from datetime import date

import yaml


sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))  # OK


from simple_ass_mat.controller import factory  # nopep8 # noqa: E402
from simple_ass_mat.controller.pajemploi_declaration import PajemploiDeclaration  # nopep8 # noqa: E402


class TestParentUsecase1(unittest.TestCase):
    """Test parent usecase 1"""

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_parent_usecase_1.yml"
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
        self.assertEqual(self.planning.annees.get_semaines_travaillees_count(), 43)
        self.assertEqual(self.planning.semaines.get_heures_travaillees(0), 37.75)
        self.assertAlmostEqual(self.planning.get_heures_travaillees_mois_mensualisees(), 135.27, delta=0.01)
        self.assertAlmostEqual(self.contrat.get_salaire_net_mensualise(), 433.26, delta=0.01)
        self.assertAlmostEqual(self.planning.get_jours_travailles_mois_mensualise(), 14.33, delta=0.01)

    def test_2023_01(self):
        """2023-01"""
        mois_courant = date(2023, 1, 1)
        today = date(2023, 2, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue
        remuneration = declaration.remuneration
        heures_majorees_ou_complementaires = declaration.heures_majorees_ou_complementaires
        indemnites_complementaires = declaration.indemnites_complementaires

        self.assertEqual(travail_effectue.nombre_heures_normales, 135)
        self.assertEqual(travail_effectue.nombre_jours_activite, 15)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertTrue(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 433.26 + 4.80, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 65.07, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertFalse(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 1.5)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 0)
        self.assertEqual(indemnites_complementaires.indemnite_kilometrique, 0)

    def test_2023_02(self):
        """2023-02"""
        mois_courant = date(2023, 2, 1)
        today = date(2023, 3, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue
        remuneration = declaration.remuneration
        heures_majorees_ou_complementaires = declaration.heures_majorees_ou_complementaires
        indemnites_complementaires = declaration.indemnites_complementaires

        self.assertEqual(travail_effectue.nombre_heures_normales, 135)
        self.assertEqual(travail_effectue.nombre_jours_activite, 15)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertTrue(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 433.26 + 2.40, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 41.81, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertFalse(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 0.75)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 0)
        self.assertEqual(indemnites_complementaires.indemnite_kilometrique, 0)

    def test_2023_03(self):
        """2023-03"""
        mois_courant = date(2023, 3, 1)
        today = date(2023, 4, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue
        remuneration = declaration.remuneration
        heures_majorees_ou_complementaires = declaration.heures_majorees_ou_complementaires
        indemnites_complementaires = declaration.indemnites_complementaires

        self.assertEqual(travail_effectue.nombre_heures_normales, 135)
        self.assertEqual(travail_effectue.nombre_jours_activite, 15)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertTrue(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 433.26 + 2.40, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 72.09, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertFalse(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 0.75)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 0)
        self.assertEqual(indemnites_complementaires.indemnite_kilometrique, 0)

    def test_2023_04(self):
        """2023-04"""
        mois_courant = date(2023, 4, 1)
        today = date(2023, 5, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue
        remuneration = declaration.remuneration
        heures_majorees_ou_complementaires = declaration.heures_majorees_ou_complementaires
        indemnites_complementaires = declaration.indemnites_complementaires

        self.assertEqual(travail_effectue.nombre_heures_normales, 135)
        self.assertEqual(travail_effectue.nombre_jours_activite, 15)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertTrue(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 433.26 + 4, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 42.01, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertFalse(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 1.25)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 0)
        self.assertEqual(indemnites_complementaires.indemnite_kilometrique, 0)

    def test_2023_05(self):
        """2023-05"""
        mois_courant = date(2023, 5, 1)
        today = date(2023, 6, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue
        remuneration = declaration.remuneration
        heures_majorees_ou_complementaires = declaration.heures_majorees_ou_complementaires
        indemnites_complementaires = declaration.indemnites_complementaires

        self.assertEqual(travail_effectue.nombre_heures_normales, 135)
        self.assertEqual(travail_effectue.nombre_jours_activite, 15)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertTrue(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 433.26 + 4, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 61.91, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertFalse(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 1.25)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 0)
        self.assertEqual(indemnites_complementaires.indemnite_kilometrique, 0)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, 'fr-FR')

    import logging
    logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler(sys.stdout)])

    unittest.main()
