"""
:date 2023-08-04
:author Nicolas Boutin
"""

# pylint: disable=logging-fstring-interpolation
# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import datetime
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))  # OK


from simple_ass_mat.controller import helper  # nopep8 # noqa: E402


class TestGetLastDayOfWeek(unittest.TestCase):
    def test_first_week_of_year(self):
        year = 2022
        week = 1
        self.assertEqual(helper.get_last_day_of_week(year, week), datetime.date(year, 1, 9))

    def test_last_week_of_year(self):
        year = 2022
        week = 52
        self.assertEqual(helper.get_last_day_of_week(year, week), datetime.date(year+1, 1, 1))

    def test_week_in_middle_of_year(self):
        year = 2022
        week = 26
        self.assertEqual(helper.get_last_day_of_week(year, week), datetime.date(year, 7, 3))

    def test_leap_year(self):
        year = 2024
        week = 9
        self.assertEqual(helper.get_last_day_of_week(year, week), datetime.date(year, 3, 3))


class TestControllerHelper(unittest.TestCase):
    """Test controller.helper"""

    def test_get_week_numbers(self):

        self.assertListEqual(helper.get_week_numbers(2022, 12), [48, 49, 50, 51])
        self.assertListEqual(helper.get_week_numbers(2023, 1), [52, 1, 2, 3, 4])
        self.assertListEqual(helper.get_week_numbers(2023, 2), [5, 6, 7, 8])
        self.assertListEqual(helper.get_week_numbers(2023, 3), [9, 10, 11, 12])
        self.assertListEqual(helper.get_week_numbers(2023, 4), [13, 14, 15, 16, 17])
        self.assertListEqual(helper.get_week_numbers(2023, 5), [18, 19, 20, 21])
        self.assertListEqual(helper.get_week_numbers(2023, 6), [22, 23, 24, 25])
        self.assertListEqual(helper.get_week_numbers(2023, 7), [26, 27, 28, 29, 30])
        self.assertListEqual(helper.get_week_numbers(2023, 8), [31, 32, 33, 34])
        self.assertListEqual(helper.get_week_numbers(2023, 9), [35, 36, 37, 38])
        self.assertListEqual(helper.get_week_numbers(2023, 10), [39, 40, 41, 42, 43])
        self.assertListEqual(helper.get_week_numbers(2023, 11), [44, 45, 46, 47])
        self.assertListEqual(helper.get_week_numbers(2023, 12), [48, 49, 50, 51, 52])
        self.assertListEqual(helper.get_week_numbers(2024, 1), [1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()
