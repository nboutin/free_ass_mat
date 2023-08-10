"""
Author: Nicolas Boutin
Date: 2023-08
Description: Represent contrat entre parent employeur et ass.mat.
"""


from .remuneration import Remuneration


class Contrat:
    """Contrat pour un enfant entre parent employeur et ass.mat."""

    def __init__(self, remuneration: Remuneration) -> None:
        self._remuneration = remuneration
