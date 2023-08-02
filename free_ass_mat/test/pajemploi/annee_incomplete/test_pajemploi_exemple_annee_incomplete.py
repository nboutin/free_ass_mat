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


sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))  # OK


import controller.factory as factory  # nopep8 # noqa: E402
from controller.pajemploi_declaration import PajemploiDeclaration  # nopep8 # noqa: E402


class TestPajemploiExempleAnneeIncomplete(unittest.TestCase):
    """Test Pajemploi exemple annee incomplete
    ExempleRemunerationAnneeIncompleteAMA.pdf"""

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_pajemploi_exemple_annee_incomplete.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contrat = factory.make_contrat(data['contrat'])
        self.planning = self.contrat.planning
        self.garde = self.contrat.garde

        self.pajemploi_declaration = PajemploiDeclaration(self.contrat)

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
        self.assertFalse(self.planning.is_annee_complete())
        self.assertEqual(self.planning.get_semaines_travaillees_annee(), 37)
        self.assertEqual(self.planning.get_heures_travaillees_semaine_par_id(), 40)
        self.assertAlmostEqual(self.planning.get_heures_travaillees_mois_mensualisees(), 123.33, delta=0.01)
        self.assertEqual(self.contrat.get_salaire_net_mensualise(), 370)
        self.assertAlmostEqual(self.planning.get_jours_travailles_mois_mensualise(), 12.33, delta=0.01)

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

        self.assertEqual(self.garde.get_heures_complementaires_semaine(2023, week_number), 5)
        self.assertEqual(self.garde.get_heures_complementaires_mois(mois_courant), 5)
        self.assertEqual(self.garde.get_heures_majorees_semaine(2023, week_number), 5)
        self.assertEqual(self.garde.get_heures_majorees_mois(mois_courant), 5)
        self.assertEqual(self.contrat.get_salaire_net_mois(mois_courant), 403.50)

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

    def test_absence_non_remunerees(self):
        """Mois suivant, AssMat absente pendant 2 semaines
        Pas de garde enfant pendant 8 jours * 10h, soit 80h.
        Ce mois, AssMat aurait du garder l'enfant 16 jours * 8h, soit 160h.
        or elle ne le garde que 8 jours
        Salaire net 185€ (370 - (370*8/16))
        Declaration Pajemploi:
        - Nombre d'heures normales = 61.66 arrondi 62h
        - Nombre de jours d'activités = 8
        - Salaire net total = 185€
        """
        mois_courant = date(2023, 4, 1)
        today = date(2023, 4, 7)

        self.assertEqual(self.garde.get_jour_absence_non_remuneree_mois(mois_courant), 8)
        self.assertEqual(self.garde.get_heure_absence_non_remuneree_mois(mois_courant), 80)
        self.assertEqual(self.planning.get_jour_travaille_prevu_mois_par_date(mois_courant), 16)
        self.assertEqual(self.planning.get_heure_travaille_prevu_mois_par_date(mois_courant), 160)
        self.assertAlmostEqual(self.contrat.get_salaire_net_mois(mois_courant), 185, delta=0.01)

        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)
        travail_effectue = declaration.travail_effectue
        remuneration = declaration.remuneration

        self.assertEqual(travail_effectue.nombre_heures_normales, 62)
        self.assertEqual(travail_effectue.nombre_jours_activite, 8)

        self.assertEqual(remuneration.salaire_net, 185)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')

    unittest.main()
