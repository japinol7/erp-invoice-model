"""Module sale_invoice.
Implements the model sale_invoice.
Depends on:
  - modules.account
  - modules.contacts
"""

__author__ = 'Joan A. Pinol  (japinol)'


from modules.account.models.account_invoice import AccountInvoice
from modules.account.models.account_invoice import AccountInvoiceType, AccountInvoiceException
from modules.sale.models.sale_invoice_line import SaleInvoiceLine


class SaleInvoice(AccountInvoice):
    """Represents a sale invoice.
       - field products_qty: A sequence with a sequence of products and their quantities.
           It is used to create the invoice lines when a new invoice is created.
           ex: 2 sodas and 3 beers: ((product_soda, 2), (product_beer, 3))
    """

    def __init__(self, invoice_id, company, client, products_qty):
        # Out invoices, i.e., sale invoices will have the prefix 'INV/OUT/' in their id
        invoice_id = 'INV/OUT/' + str(invoice_id)
        super().__init__(invoice_id, company, client, products_qty)
        self.invoice_type = AccountInvoiceType.OUT

    def add_line(self, product, qty):
        """Overrides add_line so the line added will be of type SaleInvoiceLine.
        Adds a line to the invoice.
        If the product already exists in another line, updates that line adding qty to it.
        """
        # Validates that the line can be added
        if self.is_validated:
            raise AccountInvoiceException(f"Error! You cannot add a line to a validated invoice!: {self.id}")
        elif self.is_cancelled:
            raise AccountInvoiceException(f"Error! You cannot add a line to a cancelled invoice!: {self.id}")

        for line in self.lines:
            if line.product == product:
                line.qty += qty
                break
        else:
            self.lines.append(SaleInvoiceLine(self.id, product, qty))
        self._compute_amount()
