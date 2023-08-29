"""
:date 2023-08
:author Nicolas Boutin
"""
# pylint: disable=logging-fstring-interpolation
# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from simple_ass_mat.model.data_loader.yaml_schema_validator import YamlSchemaValidator  # nopep8 # noqa: E402


class TestFullYamlSchema(unittest.TestCase):

    def test_all_fields_are_present(self):
        """001"""
        data = {
            "contrat": {
                'description': 'some description',
                'remuneration': {
                    'salaire_horaire_brut': 0.0,
                },
                'planning': {
                    'jours_type': {
                        0: ["08:00", "17:00"]
                    },
                    'semaines_type': {
                        0: {
                            'lundi': 0,
                            'mardi': None,
                            'mercredi': 0,
                            'jeudi': 0,
                            'vendredi': 0,
                            'samedi': None,
                            'dimanche': None,
                        }
                    },
                    'semaines_presences': {0: [1]},
                    'conges_payes': [2],
                },
            },
        }

        yaml_validator = YamlSchemaValidator()
        self.assertTrue(yaml_validator.validate(data))


if __name__ == '__main__':
    import logging
    # from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')
    ])

    unittest.main()
