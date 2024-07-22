"""Tests model sale_invoice.
Coding: utf-8
Author: 'Joan A. Pinol  (japinol)'
"""

__author__ = "Joan A. Pinol  (japinol)"

import unittest

from addons.contacts.models.contact import Contact
from addons.product.models.product import Product
from addons.sale.models.sale_invoice import SaleInvoice
from addons.account.models.account_invoice import AccountInvoiceType


class TestSaleInvoice(unittest.TestCase):
    def setUp(self):
        """Sets up a company, a client and some products."""
        self.company = Contact(
            "Company_assignment", "info@company_assignment.com", vat="89735694-U"
        )
        self.client = Contact(
            "Cool Beverage Company SL",
            "billing@coolbeveragecompany.com",
            vat="27956677-I",
        )
        self.soda = Product("Soda", 10.02)
        self.beer = Product("Beer", 20, "A middle quality beer")
        self.cola = Product("Cola", 9.85)
        self.water_1l = Product("Water 1L", 3)

    def test_create_invoice(self):
        """Tests the creation of an invoice."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice = SaleInvoice("1A", self.company, self.client, products)
        invoice_str = (
            f"{'-' * 40}\n"
            "Invoice # INV/OUT/1A\n"
            "  Company: Company_assignment\n"
            "           info@company_assignment.com\n"
            "  Client:  Cool Beverage Company SL\n"
            "           billing@coolbeveragecompany.com\n"
            "\n"
            "\tProduct          Price    Qty.\n"
            f"\t{'-' * 30}\n"
            "\tSoda             10.02  x  1\n"
            "\tBeer             20.00  x  2\n"
            "\tWater 1L          3.00  x  1\n"
            "\n  Total:    53.02\n"
            f"{'-' * 40}"
        )
        self.assertEqual(str(invoice), invoice_str)

    def test_invoice_type(self):
        """Tests that a created sale invoice is of type out invoice."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1), (self.cola, 3))
        invoice = SaleInvoice("1A", self.company, self.client, products)

        self.assertEqual(invoice.invoice_type, AccountInvoiceType.OUT)

    def test_invoice_write_to_db(self):
        """Tests write_to_db."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice = SaleInvoice("1A", self.company, self.client, products)

        invoice.write_to_db()


if __name__ == "__main__":
    unittest.main()
