"""
:author Nicolas Boutin
:date 2023-07-05
"""

import yaml
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # OK

import unittest  # nopep8

import controller.contract_factory as contract_factory  # nopep8


class TestSchedule(unittest.TestCase):

    def setUp(self):
        with open('schedule_data.yml', 'r', encoding='UTF-8') as file:
            schedule_data = yaml.safe_load(file)
        self.schedule = contract_factory.make_schedule(schedule_data)

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")


if __name__ == '__main__':
    unittest.main()
