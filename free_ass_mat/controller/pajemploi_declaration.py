"""
:author Nicolas Boutin
:datetime.date 2023-07-07
"""
# pylint: disable=logging-fstring-interpolation

import logging
import datetime
import math
from typing import NamedTuple

# import controller.helper as helper
from controller.contrat import Contrat

logger = logging.getLogger(__name__)


class TravailEffectue(NamedTuple):
    """Section Travail effectue de la declaration Pajemploi"""
    periode_d_emploi: datetime.date
    date_de_paiement: datetime.date
    nombre_heures_normales: int
    nombre_jours_activite: int
    nombre_jours_conges_payes: float
    avec_heures_complementaires_ou_majorees: bool
    avec_heures_specifiques: bool


class Remuneration(NamedTuple):
    """Section Remuneration de la declaration Pajemploi"""
    salaire_net: float
    indemnite_entretien: float
    avec_acompte_verse_au_salarie: bool
    avec_indemnite_repas_ou_kilometrique: bool


class HeuresMajoreesOuComplementaires(NamedTuple):
    """Section Heures Majorees Ou Complementaires de la declaration Pajemploi"""
    salaire_horaire_net: float
    nombre_heures_majorees: int
    nombre_heures_complementaires: int


class Declaration(NamedTuple):
    """Pajemploi Declaration Rapport"""
    travail_effectue: TravailEffectue
    remuneration: Remuneration
    heures_majorees_ou_complementaires: HeuresMajoreesOuComplementaires


class PajemploiDeclaration:
    """Format data pour la declaration Pajemploi"""

    def __init__(self, contrat: Contrat):
        self._contrat = contrat

    def get_declaration(self, mois_courant: datetime.date, today: datetime.date) -> Declaration:
        """Make PajemploiData"""
        return Declaration(
            travail_effectue=self._get_travail_effectue(mois_courant, today),
            remuneration=self._get_remuneration(mois_courant),
            heures_majorees_ou_complementaires=self._get_heures_majorees_ou_complementaires(mois_courant)
        )

    def _get_travail_effectue(self, mois_courant: datetime.date, today: datetime.date) -> TravailEffectue:
        """Make TravailEffectue"""
        return TravailEffectue(
            periode_d_emploi=(mois_courant.year, mois_courant.month, 1),
            date_de_paiement=today,
            nombre_heures_normales=self._get_nombre_heures_normales(mois_courant),
            nombre_jours_activite=self._get_nombre_jours_activite(mois_courant),
            nombre_jours_conges_payes=0,
            avec_heures_complementaires_ou_majorees=self._contrat.garde.has_heures_complementaires_mois(mois_courant),
            avec_heures_specifiques=False
        )

    def _get_remuneration(self, mois_courant: datetime.date) -> Remuneration:
        """Make Remuneration"""
        return Remuneration(
            salaire_net=self._contrat.get_salaire_net_mois_par_date(mois_courant),
            indemnite_entretien=self._contrat.get_frais_entretien_mois_par_date(mois_courant),
            avec_acompte_verse_au_salarie=False,
            avec_indemnite_repas_ou_kilometrique=False
        )

    def _get_heures_majorees_ou_complementaires(self, mois_courant: datetime.date) -> HeuresMajoreesOuComplementaires:
        """Make HeuresMajoreesOuComplementaires"""
        return HeuresMajoreesOuComplementaires(
            salaire_horaire_net=self._contrat.salaires_horaires.horaire_net,
            nombre_heures_majorees=self._contrat.garde.get_heures_majorees_mois_par_date(mois_courant),
            nombre_heures_complementaires=self._contrat.garde.get_heures_complementaires_mois_par_date(mois_courant)
        )

    def _get_nombre_heures_normales(self, mois_courant: datetime.date) -> int:
        """Compute the number of normal hours worked for a given month
        « Nombre d heures normales » : Salaire mensuel ÷ Taux horaire net"""

        if not self._contrat.garde.has_jour_absence_non_remuneree_mois(mois_courant):
            return round(self._contrat.planning.get_heures_travaillees_mois_mensualisees())
        else:
            return round(self._contrat.get_salaire_net_mois_par_date(mois_courant)
                         / self._contrat.salaires_horaires.horaire_net)

    def _get_nombre_jours_activite(self, mois_courant: datetime.date) -> int:
        """Compute the number of days worked for a given month
        « Nombre de jours d activité » : Nombre d heures normales ÷ Nombre d heures par jour"""

        if not self._contrat.garde.has_jour_absence_non_remuneree_mois(mois_courant):
            return math.ceil(self._contrat.planning.get_jours_travailles_mois_mensualise())
        else:
            return (self._contrat.planning.get_jours_travailles_planifies_mois_par_date(mois_courant)
                    - self._contrat.garde.get_jour_absence_non_remuneree_mois(mois_courant))
