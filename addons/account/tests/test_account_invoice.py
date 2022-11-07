"""Tests model account_invoice.
Coding: utf-8
Author: 'Joan A. Pinol  (japinol)'
"""

__author__ = 'Joan A. Pinol  (japinol)'

from decimal import Decimal
import unittest

from addons.contacts.models.contact import Contact
from addons.product.models.product import Product
from addons.account.models.account_invoice import AccountInvoice, DECIMALS_CALC


class TestAccountInvoice(unittest.TestCase):

    def setUp(self):
        """Sets up a company, a client and some products."""
        self.company = Contact('Company_assignment', 'info@company_assignment.com', vat='89735694-U')
        self.client = Contact('Cool Beverage Company SL', 'billing@coolbeveragecompany.com', vat='27956677-I')
        self.soda = Product('Soda', 10.02)
        self.beer = Product('Beer', 20, 'A middle quality beer')
        self.cola = Product('Cola', 9.85)
        self.water_1l = Product('Water 1L', 3)

    def test_create_invoice(self):
        """Tests the creation of an invoice."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice = AccountInvoice('1A', self.company, self.client, products)
        invoice_str = f"{'-' * 40}\n" \
                      "Invoice # 1A\n" \
                      "  Company: Company_assignment\n" \
                      "           info@company_assignment.com\n" \
                      "  Client:  Cool Beverage Company SL\n" \
                      "           billing@coolbeveragecompany.com\n" \
                      "\n" \
                      "\tProduct          Price    Qty.\n" \
                      f"\t{'-' * 30}\n" \
                      "\tSoda             10.02  x  1\n" \
                      "\tBeer             20.00  x  2\n" \
                      "\tWater 1L          3.00  x  1\n" \
                      "\n  Total:    53.02\n" \
                      f"{'-' * 40}"
        self.assertEqual(str(invoice), invoice_str)

    def test_create_invoice_when_original_values_have_changed(self):
        """Tests the creation of two invoices changing the original attributes
        of products and contacts:
          - Creates first invoice.
          - Changes some original attributes from products and contacts.
          - Creates second invoice.
          - Check that both invoices have the correct attributes.
        """
        # Create first invoice
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice1 = AccountInvoice('1A', self.company, self.client, products)
        invoice1_str = f"{'-' * 40}\n" \
                       "Invoice # 1A\n" \
                       "  Company: Company_assignment\n" \
                       "           info@company_assignment.com\n" \
                       "  Client:  Cool Beverage Company SL\n" \
                       "           billing@coolbeveragecompany.com\n" \
                       "\n" \
                       "\tProduct          Price    Qty.\n" \
                       f"\t{'-' * 30}\n" \
                       "\tSoda             10.02  x  1\n" \
                       "\tBeer             20.00  x  2\n" \
                       "\tWater 1L          3.00  x  1\n" \
                       "\n  Total:    53.02\n" \
                       f"{'-' * 40}"

        # Change price of soda
        self.soda.price = 15
        # Change name of company
        self.company.name = 'King_Quest'
        # Change name of client
        self.client.name = 'Small Beverage Co'

        # Create second invoice
        products2 = ((self.soda, 4), (self.beer, 3))
        invoice2 = AccountInvoice('2A', self.company, self.client, products2)
        invoice2_str = f"{'-' * 40}\n" \
                       "Invoice # 2A\n" \
                       "  Company: King_Quest\n" \
                       "           info@company_assignment.com\n" \
                       "  Client:  Small Beverage Co\n" \
                       "           billing@coolbeveragecompany.com\n" \
                       "\n" \
                       "\tProduct          Price    Qty.\n" \
                       f"\t{'-' * 30}\n" \
                       "\tSoda             15.00  x  4\n" \
                       "\tBeer             20.00  x  3\n" \
                       "\n  Total:   120.00\n" \
                       f"{'-' * 40}"

        # Check that both invoices have the correct values
        self.assertEqual(str(invoice1), invoice1_str)
        self.assertEqual(str(invoice2), invoice2_str)

    def test_invoice_add_lines(self):
        """Tests invoice add lines."""
        products = ((self.soda, 1), (self.beer, 3), (self.water_1l, 1))
        invoice = AccountInvoice('1A', self.company, self.client, products)
        new_lines = ((self.cola, 1), (self.water_1l, 1))
        invoice_str = f"{'-' * 40}\n" \
                      "Invoice # 1A\n" \
                      "  Company: Company_assignment\n" \
                      "           info@company_assignment.com\n" \
                      "  Client:  Cool Beverage Company SL\n" \
                      "           billing@coolbeveragecompany.com\n" \
                      "\n" \
                      "\tProduct          Price    Qty.\n" \
                      f"\t{'-' * 30}\n" \
                      "\tSoda             10.02  x  1\n" \
                      "\tBeer             20.00  x  3\n" \
                      "\tWater 1L          3.00  x  2\n" \
                      "\tCola              9.85  x  1\n" \
                      "\n  Total:    85.87\n" \
                      f"{'-' * 40}"

        # Check add lines with a product already in a line and a new product
        invoice.add_lines(new_lines)
        self.assertEqual(str(invoice), invoice_str)

    def test_invoice_amount(self):
        """Tests invoice amount."""
        products = ((self.soda, 2), (self.beer, 3), (self.water_1l, 1))
        self.soda.price = 5.22
        invoice = AccountInvoice('1A', self.company, self.client, products)
        self.assertEqual(invoice.amount_total, round(Decimal(73.44), DECIMALS_CALC))

    def test_validate_validated_invoice(self):
        """Tests exception thrown when trying to validate an invoice already validated."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice = AccountInvoice('1A', self.company, self.client, products)
        invoice.validate()

        # Check Exception's message raised when trying to validate an invoice already validated
        with self.assertRaises(Exception) as err:
            invoice.validate()
        self.assertEqual(str(err.exception), f"Error! This invoice has already been validated!: {invoice.id}")

    def test_validate_empty_invoice(self):
        """Tests exception thrown when trying to validate an empty invoice."""
        products = ()
        invoice = AccountInvoice('1A', self.company, self.client, products)

        # Check Exception's message raised when trying to validate an empty invoice
        with self.assertRaises(Exception) as err:
            invoice.validate()
        self.assertEqual(str(err.exception), f"Error! This invoice is empty; you cannot validate it! : {invoice.id}")

    def test_cancel_validated_invoice(self):
        """Tests exception thrown when trying to cancel a validated invoice."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice = AccountInvoice('1A', self.company, self.client, products)
        invoice.validate()

        # Check Exception's message raised when trying to  cancel a validated invoice
        with self.assertRaises(Exception) as err:
            invoice.cancel()
        self.assertEqual(str(err.exception), f"Error! Cannot cancel a validated invoice!: {invoice.id}")

    def test_pay_paid_invoice(self):
        """Tests exception thrown when trying to pay an invoice already paid."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice = AccountInvoice('1A', self.company, self.client, products)
        invoice.validate()
        invoice.pay()

        # Check Exception's message raised when trying to pay an invoice already paid
        with self.assertRaises(Exception) as err:
            invoice.pay()
        self.assertEqual(str(err.exception), f"Error! This invoice has already been paid!: {invoice.id}")

    def test_pay_non_validated_invoice(self):
        """Tests exception thrown when trying to pay an invoice not yet validated."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice = AccountInvoice('1A', self.company, self.client, products)

        # Check Exception's message raised when trying to pay an invoice not yet validated
        with self.assertRaises(Exception) as err:
            invoice.pay()
        self.assertEqual(str(err.exception), f"Error! Cannot pay a not validated invoice!: {invoice.id}")

    def test_add_line_to_validated_invoice(self):
        """Tests exception thrown when trying to add a line to a validated invoice."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice = AccountInvoice('1A', self.company, self.client, products)
        invoice.validate()

        # Check Exception's message raised when trying to add a line to a validated invoice
        with self.assertRaises(Exception) as err:
            invoice.add_line(self.cola, 2)
        self.assertEqual(str(err.exception), f"Error! You cannot add a line to a validated invoice!: {invoice.id}")

    def test_add_line_to_cancelled_invoice(self):
        """Tests exception thrown when trying to add a line to a cancelled invoice."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice = AccountInvoice('1A', self.company, self.client, products)
        invoice.cancel()

        # Check Exception's message raised when trying to add a line to a cancelled invoice
        with self.assertRaises(Exception) as err:
            invoice.add_line(self.cola, 2)
        self.assertEqual(str(err.exception), f"Error! You cannot add a line to a cancelled invoice!: {invoice.id}")

    def test_invoice_write_to_db(self):
        """Tests write_to_db."""
        products = ((self.soda, 1), (self.beer, 2), (self.water_1l, 1))
        invoice = AccountInvoice('1A', self.company, self.client, products)

        invoice.write_to_db()


if __name__ == '__main__':
    unittest.main()
