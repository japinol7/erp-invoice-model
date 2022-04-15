"""Tests model product.
Coding: utf-8
Author: 'Joan A. Pinol  (japinol)'
"""

__author__ = 'Joan A. Pinol  (japinol)'

import unittest

from modules.product.models.product import Product


class TestAccountInvoice(unittest.TestCase):

    def test_create_product(self):
        """Tests the creation of a product."""
        soda = Product('Soda', 10.02, 'Normal soda')

        self.assertEqual(soda.name, 'Soda')
        self.assertEqual(soda.price, 10.02)
        self.assertEqual(soda.description, 'Normal soda')


if __name__ == '__main__':
    unittest.main()
