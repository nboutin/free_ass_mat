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

SemainesPresenceType = dict[int, list]

SemaineType = dict[str, int]

JourType = dict[int, list] | None


class IDataLoader(ABC):
    """Interface Data Loader"""

    @abstractmethod
    def load(self, filepath: Path):
        """Load data"""

    @abstractmethod
    def get_remuneration_data(self) -> RemunerationDataType:
        """Return remuneration data"""

    @abstractmethod
    def get_semaines_presences_data(self) -> SemainesPresenceType:
        """Return semaines presences data"""

    @abstractmethod
    def get_semaine_type_data(self, semaine_id: int) -> SemaineType:
        """Return semaines type data"""

    @abstractmethod
    def get_jour_type_data(self, jour_id: int) -> JourType:
        """Return jour type data"""
