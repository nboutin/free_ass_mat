"""
Author: Nicolas Boutin
Date: 2023-08
Description: Module to handle all data
"""

from pathlib import Path

import yaml


class Model:
    """"Handle read and write to/from data"""

    def __init__(self):
        pass

    def load_user_file(self, filepath: Path):
        """Load user file"""
        with open(filepath, "r", encoding="utf-8") as file:
            user_data = yaml.safe_load(file)
