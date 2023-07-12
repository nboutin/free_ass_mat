"""
:date 2023-07-11
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


sys.path.append(os.path.join(os.path.dirname(__file__), "../../../.."))  # OK


import controller.factory as factory  # nopep8 # noqa: E402
from controller.pajemploi_declaration import PajemploiDeclaration, Remuneration  # nopep8 # noqa: E402


class TestPajemploiExempleAnneeIncomplete(unittest.TestCase):
    """Test Pajemploi exemple annee incomplete
    ExempleRemunerationAnneeIncompleteAMA.pdf"""

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_pajemploi_exemple_annee_incomplete.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contract = factory.make_contract(data['contract'])
        self.schedule = self.contract.schedule
        self.garde = self.contract.garde

        self.pajemploi_declaration = PajemploiDeclaration(self.contract)

    def test_calcul_annee_incomplete(self):
        """annee incomplete
        37 semaines travaillées
        Lundi, Mardi, Jeudi, Vendredi 8h30-18h30, 40h/semaine
        Salaire net horaire 3.00€
        Heure complémentaire 3.20€
        Heure majorée 3.50€
        Nombre heure par mensualise = 123.33
        Salaire net mensualisé = 370€
        Nombre de jours activités mensualises = 12.33
        Declaration Pajemploi:
        - Nombre d'heures normales = 123
        - Nombre de jours d'activités = 13
        """
        self.assertFalse(self.schedule.is_annee_complete())
        self.assertEqual(self.schedule.get_semaine_travaillee_annee(), 37)
        self.assertEqual(self.schedule.get_heure_travaillee_semaine_par_id(), 40)
        self.assertAlmostEqual(self.schedule.get_heure_travaille_mois_mensualisee(), 123.33, delta=0.01)
        self.assertEqual(self.contract.get_salaire_net_mensualise(), 370)
        self.assertAlmostEqual(self.schedule.get_jour_travaille_mois_mensualisee(), 12.33, delta=0.01)

        mois_courant = date(2023, 1, 1)
        today = date(2023, 1, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue

        self.assertEqual(travail_effectue.nombre_heures_normales, 123)
        self.assertEqual(travail_effectue.nombre_jours_activite, 13)

    def test_heures_complementaires_majorees(self):
        """AssMat garde enfant le mois suivant 50h au lieu de 40h pendant la deuxieme semaine
        heures complementaires 5h
        heures majorees 5h
        salaire net 403.50€
        """
        mois_courant = date(2023, 2, 1)
        week_number = 6

        self.assertEqual(self.garde.get_heure_complementaire_semaine(2023, week_number), 5)
        self.assertEqual(self.garde.get_heure_complementaire_mois(mois_courant), 5)
        self.assertEqual(self.garde.get_heure_majoree_semaine(2023, week_number), 5)
        self.assertEqual(self.garde.get_heure_majoree_mois(mois_courant), 5)
        self.assertEqual(self.contract.get_salaire_net_mois(mois_courant), 403.50)

        mois_courant = date(2023, 2, 1)
        today = date(2023, 2, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue
        remuneration = declaration.remuneration
        heures_majorees_ou_complementaires = declaration.heures_majorees_ou_complementaires

        self.assertEqual(travail_effectue.nombre_heures_normales, 123)
        self.assertEqual(travail_effectue.nombre_jours_activite, 13)
        self.assertTrue(travail_effectue.avec_heures_complementaires_ou_majorees)

        self.assertEqual(remuneration.salaire_net, 403.50)

        self.assertEqual(heures_majorees_ou_complementaires.salaire_horaire_net, 3.00)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_majorees, 5)
        self.assertEqual(heures_majorees_ou_complementaires.nombre_heures_complementaires, 5)

    # def test_absence_non_remunerees(self):
    #     """Mois suivant, AssMat absente pendant 2 semaines
    #     Pas de garde enfant pendant 8 jours * 8h, soit 64h.
    #     Ce mois, AssMat aurait du garder l'enfant 17 jours * 8h, soit 136h.
    #     or elle ne le garde que 9 jours
    #     """
    #     mois_courant = date(2023, 9, 1)
    #     today = date(2023, 7, 7)

    #     self.assertEqual(self.garde.get_jour_absence_non_remuneree_mois(mois_courant), 8)
    #     self.assertEqual(self.garde.get_heure_absence_non_remuneree_mois(mois_courant), 64)
    #     self.assertEqual(self.schedule.get_jour_travaille_prevu_mois_par_date(mois_courant), 17)
    #     self.assertEqual(self.schedule.get_heure_travaille_prevu_mois_par_date(mois_courant), 136)
    #     self.assertAlmostEqual(self.contract.get_salaire_net_mois(mois_courant), 220.24, delta=0.01)

    #     declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)

    #     self.assertEqual(declaration.travail_effectue.nombre_heures_normales, 73)
    #     self.assertEqual(declaration.travail_effectue.nombre_jours_activite, 9)
    #     self.assertEqual(declaration.travail_effectue.nombre_jours_conges_payes, 0)
    #     self.assertEqual(declaration.travail_effectue.avec_heures_complementaires_ou_majorees, False)
    #     self.assertEqual(declaration.travail_effectue.avec_heures_specifiques, False)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')

    unittest.main()
