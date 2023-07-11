"""
:author Nicolas Boutin
:datetime.date 2023-07-07
"""
# pylint: disable=logging-fstring-interpolation

import logging
import datetime
from typing import NamedTuple

# import controller.helper as helper
from controller.contract import Contract

logger = logging.getLogger(__name__)


class TravailEffectue(NamedTuple):
    """Section Travail effectue de la declaration Pajemploi"""
    periode_d_emploi: datetime.date
    date_de_paiement: datetime.date
    nombre_heure_normal: int
    nombre_jour_activite: int
    nombre_jour_conges_payes: float
    avec_heure_complementaire_ou_majoree: bool
    avec_heure_specifique: bool


class Remuneration(NamedTuple):
    """Section Remuneration de la declaration Pajemploi"""
    salaire_net: float
    indemnite_entretien: float
    avec_acompte_verse_au_salarie: bool
    avec_indemnite_repas_ou_kilometrique: bool


class Declaration(NamedTuple):
    """Pajemploi Declaration Rapport"""
    travail_effectue: TravailEffectue
    remuneration: Remuneration


class PajemploiDeclaration:
    """Format data pour la declaration Pajemploi"""

    def __init__(self, contrat: Contract):
        self._contrat = contrat

    def get_declaration(self, mois_courant: datetime.date, today: datetime.date) -> Declaration:
        """Make PajemploiData"""
        return Declaration(
            travail_effectue=self._get_travail_effectue(mois_courant, today),
            remuneration=self._get_remuneration()
        )

    def _get_travail_effectue(self, mois_courant: datetime.date, today: datetime.date) -> TravailEffectue:
        """Make TravailEffectue"""
        return TravailEffectue(
            periode_d_emploi=(mois_courant.year, mois_courant.month, 1),
            date_de_paiement=today,
            nombre_heure_normal=self._contrat.schedule.get_heure_travaille_mois_mensualisee_normalisee(),
            nombre_jour_activite=self._contrat.schedule.get_jour_travaille_mois_mensualisee_normalise(),
            nombre_jour_conges_payes=0,
            avec_heure_complementaire_ou_majoree=False,
            avec_heure_specifique=False
        )

    def _get_remuneration(self):
        """Make Remuneration"""
        return Remuneration(
            salaire_net=self._contrat.get_salaire_net_mensualise(),
            indemnite_entretien=0.0,
            avec_acompte_verse_au_salarie=False,
            avec_indemnite_repas_ou_kilometrique=False
        )
