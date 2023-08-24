"""
Author: Nicolas Boutin
Date: 2023-08
Description:
"""

from copy import deepcopy

from .data_loader import IDataLoader
from .yaml_file_loader import YamlFileLoader
from .yaml_schema_validator import YamlSchemaValidator

from .contrat import Contrat
from .remuneration import Remuneration
from .planning import Planning, SemaineAcceuil


class DataLoaderFactory:
    """Data Loader Factory"""

    def make_data_loader(self, data_loader_type: str) -> IDataLoader:
        """Make data loader"""
        if data_loader_type == "yaml":
            validator = YamlSchemaValidator()
            return YamlFileLoader(validator)
        raise ValueError(f"Unknown data loader type: {data_loader_type}")
    

class ModelFactory:
    """Model Factory"""

    def __init__(self, data_loader: IDataLoader):
        self._data_loader = data_loader

    def make_contrat(self) -> Contrat:
        """Make contrat"""
        remuneration = self.make_remuneration(self._data_loader.get_remuneration_data())
        planning = make_planning_with_range(
            data_loader.get_semaines_acceuil_ranges(), 
            data_loader.get_semaines_conges_payes())
        return Contrat(planning=planning, remuneration=remuneration)

    def make_remuneration(self, remuneration_data) -> Remuneration:
        """Make Remuneration"""
        return Remuneration(tarif_horaire_brut=remuneration_data["tarif_horaire_brut"])


def make_planning_with_range(semaines_acceuil_ranges: dict[tuple, SemaineAcceuil], semaines_conges_payes: list[int]):
    """Make Planning avec des intervals de semaines d acceuil"""
    semaines_acceuil = {}
    for intervals, semaine_acceuil in semaines_acceuil_ranges.items():
        for semaine in range(intervals[0], intervals[1]+1):
            semaines_acceuil[semaine] = deepcopy(semaine_acceuil)
    return Planning(semaines_acceuil, semaines_conges_payes)
