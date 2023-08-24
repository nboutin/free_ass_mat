"""
Author: Nicolas Boutin
Date: 2023-08
Description:
"""

from abc import ABC, abstractmethod
from pathlib import Path

RemunerationDataType = dict[str, float]
"""
RemunerationDataType type alias

salaire_horaire_brut: float
"""


class IDataLoader(ABC):
    """Interface Data Loader"""

    @abstractmethod
    def load(self, filepath: Path):
        """Load data"""

    @abstractmethod
    def get_remuneration_data(self) -> RemunerationDataType:
        """Return remuneration data"""
