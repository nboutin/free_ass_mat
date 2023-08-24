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

    # nest schema into document key to apply rules onto root item
    schema = {
        'document': {
            'type': 'dict',
            'keysrules': {'type': 'string'},  # 'contains': 'contrat'
            'schema': {
                'contrat': {
                    'type': 'dict',
                    'keysrules': {'type': 'string'},
                    'schema': {
                        'description': {'type': 'string'},
                        'remuneration': {
                            'type': 'dict',
                            'keysrules': {'type': 'string'},
                            'schema': {
                                'salaire_horaire_brut': {'type': 'float'}
                            }
                        }
                    }
                }
            }
        }
    }

    def __init__(self) -> None:
        pass

    def validate(self, yaml_data):
        """Validate YAML data"""
        validator = Validator(self.schema, require_all=True)
        if not validator.validate({'document': yaml_data}):
            logger.error(validator.errors)
            return False
        return True
