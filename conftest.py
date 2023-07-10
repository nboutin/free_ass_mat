"""
:date 2023-07-10
:author Nicolas Boutin
"""

import locale


def pytest_configure():
    """Set the French locale"""
    locale.setlocale(locale.LC_ALL, 'fr_FR')
