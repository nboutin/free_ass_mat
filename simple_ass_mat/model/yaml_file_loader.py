"""
Author: Nicolas Boutin
Date: 2023-08
Description: YAML File loader
"""

from pathlib import Path

import yaml

from .data_loader import IDataLoader, RemunerationDataType, SemainesPresenceType, JourType, SemaineType


class FileFormatError(Exception):
    """File format error"""


class YamlFileLoader(IDataLoader):
    """YAML File loader"""

    def __init__(self, validator) -> None:
        if not validator:
            raise ValueError("Validator is mandatory for YamlFileLoader construction")

        self._data = None
        self._validator = validator

    def load(self, filepath: Path) -> None:
        """Read YAML file"""
        with open(filepath, "r", encoding="utf-8") as file:
            self._data = yaml.safe_load(file)

        if not self._validator.validate(self._data):
            raise FileFormatError(self._validator.errors)

    def get_remuneration_data(self) -> RemunerationDataType:
        """Return remuneration data"""
        return self._data["contrat"]["remuneration"]

    def get_semaines_presences_data(self) -> SemainesPresenceType:
        """Return semaines presences data"""
        return self._data["contrat"]["planning"]["semaines_presences"]

    def get_semaine_type_data(self, semaine_id: int) -> SemaineType:
        """Return semaines type data"""
        return self._data["contrat"]["planning"]["semaines_type"][semaine_id]

    def get_jour_type_data(self, jour_id: int) -> JourType:
        """Return jour type data"""
        try:
            return self._data["contrat"]["planning"]["jours_type"][jour_id]
        except KeyError:
            return None
