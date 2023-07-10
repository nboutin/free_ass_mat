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


class Pajemploi:
    """Format data pour la declaration Pajemploi"""

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

    # class PajemploiData(NamedTuple):
    #     travail_effectue: TravailEffectue
    #     remuneration: Remuneration

    def __init__(self, contrat: Contract):
        self._contrat = contrat

    # def get_pajemploi_data(self, date: datetime.date) -> PajemploiData:
    #     """Make PajemploiData"""
    #     return Pajemploi.PajemploiData(
    #         travail_effectue=self._get_travail_effectue(date),
    #         remuneration=self._get_remuneration(date)
    #     )

    # def _get_travail_effectue(self, date: datetime.date) -> TravailEffectue:
    #     """Make TravailEffectue"""
    #     return Pajemploi.TravailEffectue(
    #         periode_d_emploi=self._contrat.schedule.get_date_debut(),
    #         date_de_paiement=datetime.now(),
    #         nombre_heure_normal=self._contrat.schedule.get_heure_travaille_prevu_mois_par_date(date),
    #         nombre_jour_activite=self._contrat.schedule.get_jour_activite_mois_par_date(date),
    #         nombre_jour_conges_payes=self._contrat.schedule.get_jour_conges_payes_mois_par_date(date),
    #         avec_heure_complementaire_ou_majoree=self._contrat.schedule.get_heure_complementaire_ou_majoree_mois_par_date(
    #             date) > 0,
    #         avec_heure_specifique=self._contrat.schedule.get_heure_specifique_mois_par_date(date) > 0
    #     )
