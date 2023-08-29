"""
Author: Nicolas Boutin
Date: 2023-08
Description: YAML Schema validator
"""

import logging
from pathlib import Path

from cerberus import Validator
import yaml


logger = logging.getLogger(__name__)


class YamlSchemaValidator:
    """YAML Schema validator"""

    # nest schema into document key to apply rules onto root item
    # \todo try with schema keyword for root key
    def __init__(self) -> None:
        schema_filepath: Path = Path(__file__).parent / 'user_file_schema.yaml'

        with open(schema_filepath, 'r', encoding='utf-8') as schema_file:
            schema = yaml.safe_load(schema_file)

        self._validator = Validator(schema, require_all=True)

    @property
    def errors(self):
        """Return errors"""
        return self._validator.errors

    def validate(self, yaml_data):
        """Validate YAML data"""
        if not self._validator.validate({'document': yaml_data}):
            logger.error(self._validator.errors)
            return False
        return True
