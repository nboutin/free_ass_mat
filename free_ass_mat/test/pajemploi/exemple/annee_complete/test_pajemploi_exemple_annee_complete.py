"""
:date 2023-07-10
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
from controller.pajemploi_declaration import PajemploiDeclaration  # nopep8 # noqa: E402


class TestPajemploiExempleAnneeComplete(unittest.TestCase):
    """Test Pajemploi exemple
    ExempleRemunerationAccueilRegulierAMA.pdf"""

    def setUp(self):
        data_filepath = Path(__file__).parent / "data_pajemploi_exemple_annee_complete.yml"
        with open(data_filepath, 'r', encoding='UTF-8') as file:
            data = yaml.safe_load(file)
        self.contract = factory.make_contract(data['contract'])
        self.schedule = self.contract.schedule
        self.garde = self.contract.garde

        self.pajemploi_declaration = PajemploiDeclaration(self.contract)

    def test_calcul_annee_complete(self):
        """52 semaines, année complète
        47 semaines travaillées
        Mardi-Vendredi 9h-17h, 32h/semaine
        Salaire net horaire 3.00€
        Heure complémentaire 3.20€
        Heure majorée 3.50€
        """
        self.assertTrue(self.contract.is_complete_year())
        self.assertEqual(self.schedule.get_semaine_travaillee_annee(), 47)
        self.assertEqual(self.schedule.get_heure_travaillee_semaine_par_id(), 32)
        self.assertAlmostEqual(self.schedule.get_heure_travaille_mois_mensualisee(), 138.66, delta=0.01)
        self.assertEqual(self.contract.get_salaire_net_mensualise(), 416)

        self.assertEqual(self.schedule.get_heure_travaille_mois_mensualisee_normalisee(), 139)
        self.assertAlmostEqual(self.schedule.get_jour_travaille_mois_mensualisee(), 17.33, delta=0.01)
        self.assertEqual(self.schedule.get_jour_travaille_mois_mensualisee_normalise(), 18)

    def test_heures_complementaires_majorees(self):
        """AssMat garde enfant le mois suivant 50h au lieu de 32h pendant la deuxieme semaine"""
        self.assertEqual(self.garde.get_heure_complementaire_semaine(2023, 2), 13)
        self.assertEqual(self.garde.get_heure_complementaire_mois(date(2023, 1, 1)), 13)
        self.assertEqual(self.garde.get_heure_majoree_semaine(2023, 2), 5)
        self.assertEqual(self.garde.get_heure_majoree_mois(date(2023, 1, 1)), 5)
        self.assertEqual(self.contract.get_salaire_net_mois(date(2023, 1, 1)), 475.10)

    def test_declaration_pajemploi_heures_complementaires_majorees(self):
        """52 semaines, année complète
        47 semaines travaillées
        Mardi-Vendredi 9h-17h, 32h/semaine
        Salaire net horaire 3.00€
        Heure complémentaire 3.20€
        Heure majorée 3.50€
        AssMat garde enfant le mois suivant 50h au lieu de 32h pendant la deuxieme semaine
        """
        mois_courant = date(2023, 1, 1)
        today = date(2023, 7, 7)
        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)

        self.assertEqual(declaration.travail_effectue.nombre_heures_normales, 139)
        self.assertEqual(declaration.travail_effectue.nombre_jours_activite, 18)
        self.assertEqual(declaration.travail_effectue.nombre_jours_conges_payes, 0)
        self.assertEqual(declaration.travail_effectue.avec_heures_complementaires_ou_majorees, True)
        self.assertEqual(declaration.travail_effectue.avec_heures_specifiques, False)

    #     self.assertEqual(declaration.remuneration.salaire_net, 416)
    #     self.assertEqual(declaration.remuneration.indemnite_entretien, 0)
    #     self.assertEqual(declaration.remuneration.avec_acompte_verse_au_salarie, False)
    #     self.assertEqual(declaration.remuneration.avec_indemnite_repas_ou_kilometrique, False)

    def test_absence_non_remunerees(self):
        """Mois suivant, AssMat absente pendant 2 semaines
        Pas de garde enfant pendant 8 jours * 8h, soit 64h.
        Ce mois, AssMat aurait du garder l'enfant 17 jours * 8h, soit 136h.
        or elle ne le garde que 9 jours
        """
        mois_courant = date(2023, 9, 1)
        today = date(2023, 7, 7)

        self.assertEqual(self.garde.get_jour_absence_non_remuneree_mois(mois_courant), 8)
        self.assertEqual(self.garde.get_heure_absence_non_remuneree_mois(mois_courant), 64)
        self.assertEqual(self.schedule.get_jour_travaille_prevu_mois_par_date(mois_courant), 17)
        self.assertEqual(self.schedule.get_heure_travaille_prevu_mois_par_date(mois_courant), 136)
        self.assertAlmostEqual(self.contract.get_salaire_net_mois(mois_courant), 220.24, delta=0.01)

        declaration = self.pajemploi_declaration.get_declaration(mois_courant, today)

        self.assertEqual(declaration.travail_effectue.nombre_heures_normales, 73)
        self.assertEqual(declaration.travail_effectue.nombre_jours_activite, 9)
        self.assertEqual(declaration.travail_effectue.nombre_jours_conges_payes, 0)
        self.assertEqual(declaration.travail_effectue.avec_heures_complementaires_ou_majorees, False)
        self.assertEqual(declaration.travail_effectue.avec_heures_specifiques, False)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')

    unittest.main()
