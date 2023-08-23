"""
Author: Nicolas Boutin
Date: 2023-08
Description: Module to handle all data
"""

from pathlib import Path

import yaml


class YamlFileLoader:
    """YAML File loader"""

    def __init__(self) -> None:
        self._data = None

    def load(self, filepath: Path) -> None:
        """Read YAML file"""
        with open(filepath, "r", encoding="utf-8") as file:
            self._data = yaml.safe_load(file)

    @property
    def remuneration_data(self):
        """Return remuneration data"""
        return self._data["contrat"]["remuneration"]


    