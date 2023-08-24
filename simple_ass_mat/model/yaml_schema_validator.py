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
    # \todo try with schema keyword for root key
    schema = {
        'document': {
            'type': 'dict',
            'keysrules': {'type': 'string'},
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
                        },
                        'planning': {
                            'type': 'dict',
                            'keysrules': {'type': 'string'},
                            'schema': {
                                'jours_type': {
                                    'type': 'dict',
                                    'keysrules': {'type': 'integer'},
                                    'valuesrules': {
                                        'type': 'list',
                                        'schema': {
                                            'type': 'string',
                                        }
                                    }
                                },
                                'semaines_type': {
                                    'type': 'dict',
                                    'keysrules': {'type': 'integer'},
                                    'valuesrules': {
                                        'type': 'dict',
                                        'keysrules': {'type': 'string'},
                                        'schema': {
                                            'lundi': {'type': 'integer', 'nullable': True},
                                            'mardi': {'type': 'integer', 'nullable': True},
                                            'mercredi': {'type': 'integer', 'nullable': True},
                                            'jeudi': {'type': 'integer', 'nullable': True},
                                            'vendredi': {'type': 'integer', 'nullable': True},
                                            'samedi': {'type': 'integer', 'nullable': True},
                                            'dimanche': {'type': 'integer', 'nullable': True},
                                        }
                                    }
                                },
                                'semaines_presences': {
                                    'type': 'list',
                                    'schema': {
                                        'type': 'integer',
                                    }
                                },
                                'conges_payes': {
                                    'type': 'list',
                                    'schema': {
                                        'type': 'integer',
                                    }
                                }
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
