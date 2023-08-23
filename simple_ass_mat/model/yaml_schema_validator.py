"""
Author: Nicolas Boutin
Date: 2023-08
Description: YAML Schema validator
"""

import logging

from cerberus import Validator


logger = logging.getLogger(__name__)


class YamlSchemaValidator:
    """YAML Schema validator"""

    schema = {
        'contrat': {
            'type': 'dict',
            'keysrules': {'type': 'string', 'contains': 'contrat'},
            'schema': {
                'description': {'type': 'string'}
            }
        }
    }

    def __init__(self) -> None:
        pass

    def validate(self, yaml_data):
        """Validate YAML data"""
        validator = Validator(self.schema, require_all=True)
        if not validator.validate(yaml_data):
            logger.error(validator.errors)
