"""
Author: Nicolas Boutin
Date: 2023-08
Description:
"""


class Remuneration:
    """Handle ass mat remuneration"""

    _RATIO_BRUT_NET = 0.7812

    def __init__(self, salaire_horaire_brut: float) -> None:
        self._salaire_horaire_brut = salaire_horaire_brut

    def get_salaire_horaire_brut(self):
        """Retourne le tarif horaire brut"""
        return self._salaire_horaire_brut

    def get_salaire_horaire_net(self):
        """Retourne le salaire horaire net"""
        return self._salaire_horaire_brut * Remuneration._RATIO_BRUT_NET
