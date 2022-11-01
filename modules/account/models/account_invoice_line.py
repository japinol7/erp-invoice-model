"""Module account_invoice.
Implements the model account_invoice_line.
Coding: utf-8
Author: 'Joan A. Pinol  (japinol)'
Depends on:
  - modules.product
  - modules.base.models.db_driver
"""

__author__ = 'Joan A. Pinol  (japinol)'

from decimal import Decimal
import logging

from modules.base.models.db_driver import db_driver

# Decimal digits for intermediate calculation operations
DECIMALS_CALC = 3

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AccountInvoiceLine:
    """Represents an invoice's line."""

    def __init__(self, invoice_id, product, qty):
        self.invoice_id = invoice_id
        self.product = product
        self.product_name = product.name
        self.price = product.price
        self.qty = qty
        self.product_desc = product.description

    def __str__(self):
        return f"{self.product_name:15} {self.price:6.2f}  x{self.qty:3}"

    __repr__ = __str__

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        """price setter.
        Converts value to Decimal and rounds it to n decimals.
        """
        self._price = round(Decimal(value), DECIMALS_CALC)

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, value):
        """qty setter.
        Converts value to integer.
        """
        self._qty = int(value)

    def price_subtotal(self):
        return round(self.price * self.qty, DECIMALS_CALC)

    def write_to_db(self):
        """Writes the current fields to the database."""
        vals = {'invoice_id': self.invoice_id,
                'product_name': self.product_name,
                'price': self.price,
                'qty': self.qty,
                'product_desc': self.product_desc
                }

        db_driver.write(self.__class__.__name__, vals)
