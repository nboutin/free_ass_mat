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
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

# from simple_ass_mat.model.factory import make_planning_with_range  # nopep8 # noqa: E402
from simple_ass_mat.model.yaml_file_loader import YamlFileLoader  # nopep8 # noqa: E402


class ValidatorMock:

    def validate(self, yaml_data):
        _ = yaml_data
        return True


class TestLoad(unittest.TestCase):

    def test_remuneration_data(self):
        """
        user file contains:
        1 contrat
        """
        loader = YamlFileLoader(ValidatorMock())
        loader.load(Path(__file__).parent / "user_file" / "user_file_all_data.yml")

        remuneration_data = loader.get_remuneration_data()
        self.assertDictEqual(remuneration_data,  {'salaire_horaire_brut': 4.10})


if __name__ == '__main__':
    import logging
    # from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(Path(__file__).parent / Path(__file__ + '.log'), mode='w')
    ])

    unittest.main()
