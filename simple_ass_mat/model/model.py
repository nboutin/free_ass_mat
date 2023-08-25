"""
Author: Nicolas Boutin
Date: 2023-08
Description: Module to handle all data
"""

from .contrat import Contrat


class Model:
    """"Handle contrat"""

    def __init__(self):
        self._contrat: Contrat = None

    def add_contrat(self, contrat: Contrat) -> None:
        """Add a contrat to the model"""
        self._contrat = contrat
