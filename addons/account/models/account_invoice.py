"""Module account_invoice.
Implements the model account_invoice.
Coding: utf-8
Author: 'Joan A. Pinol  (japinol)'
Depends on:
  - modules.contacts
  - modules.base.models.db_driver
"""

__author__ = "Joan A. Pinol  (japinol)"

from builtins import isinstance
from enum import Enum

from tools.logger.logger import log as logger
from addons.account.models.account_invoice_line import AccountInvoiceLine
from addons.base.models.db_driver import db_driver

# Decimal digits for intermediate calculation operations
DECIMALS_CALC = 3


class AccountInvoiceType(Enum):
    """Invoice types."""

    IN = "in"
    OUT = "out"


class AccountInvoiceException(Exception):
    pass


class AccountInvoice:
    """Represents an invoice.
    - field products_qty: A sequence with a sequence of products and their quantities.
        It is used to create the invoice lines when a new invoice is created.
        ex: 2 sodas and 3 beers: ((product_soda, 2), (product_beer, 3))
    """

    def __init__(self, invoice_id, company, client, products_qty):
        self.id = str(invoice_id)
        self.company = company
        self.client = client
        self.company_name = company.name
        self.company_email = company.email
        self.company_vat = company.props.get("vat", "")
        self.client_name = client.name
        self.client_email = client.email
        self.client_vat = client.props.get("vat", "")
        self.amount_total = 0
        self.invoice_type = None
        self.lines = []
        self.is_cancelled = False
        self.is_paid = False
        self.is_validated = False
        self.is_sent = False

        self.add_lines(products_qty)

    def _compute_amount(self):
        """Computes amount."""
        self.amount_total = round(
            sum(line.price_subtotal() for line in self.lines), DECIMALS_CALC
        )

    def add_lines(self, products_qty):
        """Adds some lines to the invoice."""
        # Validate products_qty
        if not isinstance(products_qty, (list, tuple)):
            logger.critical(
                "Error! products_qty must be a sequence of sequences. Ex: ((product_soda, 2), (product_beer, 3))"
                f"provided: {products_qty}"
            )
            return

        for product, qty in products_qty:
            self.add_line(product, qty)

        self._compute_amount()

    def add_line(self, product, qty):
        """Adds a line to the invoice.
        If the product already exists in another line, updates that line adding qty to it.
        """
        # Validates that the line can be added
        if self.is_validated:
            raise AccountInvoiceException(
                f"Error! You cannot add a line to a validated invoice!: {self.id}"
            )
        elif self.is_cancelled:
            raise AccountInvoiceException(
                f"Error! You cannot add a line to a cancelled invoice!: {self.id}"
            )

        for line in self.lines:
            if line.product == product:
                line.qty += qty
                break
        else:
            self.lines.append(AccountInvoiceLine(self.id, product, qty))
        self._compute_amount()

    def validate(self):
        """Validates the invoice."""
        # Validates that the order can be validated
        if self.is_validated:
            raise AccountInvoiceException(
                f"Error! This invoice has already been validated!: {self.id}"
            )
        elif not self.lines:
            raise AccountInvoiceException(
                f"Error! This invoice is empty; you cannot validate it! : {self.id}"
            )

        self.is_validated = True

    def cancel(self):
        """Cancels the invoice."""
        # Validate that the order can be cancelled
        if self.is_validated:
            raise AccountInvoiceException(
                f"Error! Cannot cancel a validated invoice!: {self.id}"
            )

        self.is_cancelled = True

    def pay(self):
        """Pays the invoice."""
        # Validate that the order can be paid
        if self.is_paid:
            raise AccountInvoiceException(
                f"Error! This invoice has already been paid!: {self.id}"
            )
        elif not self.is_validated:
            raise AccountInvoiceException(
                f"Error! Cannot pay a not validated invoice!: {self.id}"
            )
        elif self.is_cancelled:
            raise AccountInvoiceException(
                f"Error! Cannot pay a cancelled invoice!: {self.id}"
            )

        self.is_paid = True

    def write_to_db(self):
        """Writes the current fields to the database.
        In this implementation, an attribute change does not trigger a database update.
        So, a call to this method is mandatory to synchronize the attributes with the database.
        """
        vals = {
            "id": self.id,
            "invoice_type": self.invoice_type and self.invoice_type.value or "",
            "company_name": self.company_name,
            "company_email": self.company_email,
            "company_vat": self.company_vat,
            "client_name": self.client_name,
            "client_email": self.client_email,
            "client_vat": self.client_vat,
            "amount_total": self.amount_total,
            "lines": self.lines,
            "is_cancelled": self.is_cancelled,
            "is_paid": self.is_paid,
            "is_validated": self.is_validated,
            "is_sent": self.is_sent,
        }

        db_driver.write(self.__class__.__name__, vals)

        for line in self.lines:
            line.write_to_db()

    def print_invoice(self):
        """Prints an invoice to the debug logging level.
        You can override this method to add actual printing invoice code.
        """
        logger.debug(f"Printing invoice: \n{str(self)}")

    def __str__(self):
        res = [
            f"{'-' * 40}",
            f"Invoice # {self.id}",
            f"  Company: {self.company_name}",
            f"           {self.company_email}",
            f"  Client:  {self.client_name}",
            f"           {self.client_email}\n",
        ]
        res += [f"\t{'Product':15} {'Price':>6} {'Qty.':>7}", f"\t{'-' * 30}"]
        for line in self.lines:
            res += [f"\t{line}"]

        res += [f"\n  Total: {self.amount_total:8.2f}", f"{'-' * 40}"]
        return "\n".join(res)

    __repr__ = __str__
