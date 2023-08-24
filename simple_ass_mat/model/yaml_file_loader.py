"""
Author: Nicolas Boutin
Date: 2023-08
Description: Module to handle all data
"""

from pathlib import Path

import yaml

from .data_loader import IDataLoader, RemunerationDataType


class FileFormatError(Exception):
    """File format error"""


class YamlFileLoader(IDataLoader):
    """YAML File loader"""

    def __init__(self, validator) -> None:
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
