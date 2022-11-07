"""Tests model db_driver.
Coding: utf-8
Author: 'Joan A. Pinol  (japinol)'
"""

__author__ = 'Joan A. Pinol  (japinol)'

import unittest

from addons.base.models.db_driver import DBDriver


class TestDBDriver(unittest.TestCase):

    def test_create_db_driver(self):
        """Tests the creation of a database driver."""
        db_driver1 = DBDriver()

        self.assertEqual(db_driver1.name, 'dummy_db')


if __name__ == '__main__':
    unittest.main()
