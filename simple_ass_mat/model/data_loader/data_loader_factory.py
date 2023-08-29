"""
Author: Nicolas Boutin
Date: 2023-08
Description:
"""

from .data_loader import IDataLoader
from .yaml_file_loader import YamlFileLoader
from .yaml_schema_validator import YamlSchemaValidator


class DataLoaderFactory:
    """Data Loader Factory"""

    @staticmethod
    def make_data_loader(data_loader_type: str) -> IDataLoader:
        """Make data loader"""
        if data_loader_type == "yaml":
            validator = YamlSchemaValidator()
            return YamlFileLoader(validator)
        raise ValueError(f"Unknown data loader type: {data_loader_type}")
