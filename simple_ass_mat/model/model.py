"""
Author: Nicolas Boutin
Date: 2023-08
Description: Module to handle all data
"""

# from pathlib import Path

from .contrat import Contrat


class Model:
    """"Handle all data type"""

    def __init__(self):
        """
        \todo use UserFileLoader interface
        """
        self._contrat: Contrat = None

    def add_contrat(self, contrat: Contrat) -> None:
        """Add a contrat to the model"""
        self._contrat = contrat
