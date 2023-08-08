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


class TestParentUsecase2(unittest.TestCase):
    """Test parent usecase 2"""

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_parent_usecase_2.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contrat = factory.make_contrat(data['contrat'])
        self.planning = self.contrat.planning
        self.garde = self.contrat.garde

        self.pajemploi_declaration = PajemploiDeclaration(self.contrat)

    def test_contrat_parametres(self):
        """Contrat parametres"""
        self.assertFalse(self.planning.is_annee_complete())
        self.assertEqual(self.planning.get_semaines_travaillees_annee(), 43)
        self.assertEqual(self.planning.get_heures_travaillees_semaine_par_id(0), 8.5)
        self.assertEqual(self.planning.get_heures_travaillees_semaine_par_id(1), 37.75)
        self.assertAlmostEqual(self.planning.get_heures_travaillees_mois_mensualisees(), 45.08, delta=0.01)
        self.assertAlmostEqual(self.contrat.get_salaire_net_mensualise(), 144.40, delta=0.01)
        self.assertAlmostEqual(self.planning.get_jours_travailles_mois_mensualise(), 5.08, delta=0.01)

    def test_2023_01(self):
        """2023-01"""
        mois_courant = date(2023, 1, 1)
        today = date(2023, 2, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue
        remuneration = declaration.remuneration
        heures_majorees_ou_complementaires = declaration.heures_majorees_ou_complementaires
        indemnites_complementaires = declaration.indemnites_complementaires

        self.assertEqual(travail_effectue.nombre_heures_normales, 45)
        self.assertEqual(travail_effectue.nombre_jours_activite, 6)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertTrue(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 144.40 + 10.5*3.2029, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 17.85, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertTrue(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 10.5)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 12)
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

        self.assertEqual(travail_effectue.nombre_heures_normales, 45)
        self.assertEqual(travail_effectue.nombre_jours_activite, 6)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertFalse(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 144.40, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 14.14, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertTrue(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 0)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 12)
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

        self.assertEqual(travail_effectue.nombre_heures_normales, 45)
        self.assertEqual(travail_effectue.nombre_jours_activite, 6)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertFalse(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 144.40, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 17.05, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertTrue(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 0)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 15)
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

        self.assertEqual(travail_effectue.nombre_heures_normales, 45)
        self.assertEqual(travail_effectue.nombre_jours_activite, 6)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertTrue(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 144.40 + .5*3.2029, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 14.34, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertTrue(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 0.5)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 12)
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

        self.assertEqual(travail_effectue.nombre_heures_normales, 45)
        self.assertEqual(travail_effectue.nombre_jours_activite, 6)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertFalse(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 144.40, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 17.40, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertTrue(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 0)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 15)
        self.assertEqual(indemnites_complementaires.indemnite_kilometrique, 0)

    @unittest.skip("TODO")
    def test_2022_12(self):
        """2022-12"""
        mois_courant = date(2022, 12, 1)
        today = date(2023, 1, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue
        remuneration = declaration.remuneration
        heures_majorees_ou_complementaires = declaration.heures_majorees_ou_complementaires
        indemnites_complementaires = declaration.indemnites_complementaires

        self.assertEqual(travail_effectue.nombre_heures_normales, 39)
        self.assertEqual(travail_effectue.nombre_jours_activite, 6)
        self.assertEqual(travail_effectue.nombre_jours_conges_payes, 0)
        self.assertFalse(travail_effectue.avec_heures_complementaires_ou_majorees)
        self.assertFalse(travail_effectue.avec_heures_specifiques)

        self.assertAlmostEqual(remuneration.salaire_net, 144.40, delta=0.01)
        self.assertAlmostEqual(remuneration.indemnite_entretien, 17.40, delta=0.01)
        self.assertFalse(remuneration.avec_acompte_verse_au_salarie)
        self.assertTrue(remuneration.avec_indemnite_repas_ou_kilometrique)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.2029)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 0)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 0)

        self.assertEqual(indemnites_complementaires.indemnite_repas, 15)
        self.assertEqual(indemnites_complementaires.indemnite_kilometrique, 0)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, 'fr-FR')

    import logging
    logging.basicConfig(level=logging.INFO, handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')])

    unittest.main()
