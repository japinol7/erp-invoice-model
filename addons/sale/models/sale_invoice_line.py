"""Module sale_invoice.
Implements the model sale_invoice.
Depends on:
  - modules.account
  - modules.product
"""

__author__ = 'Joan A. Pinol  (japinol)'


from addons.account.models.account_invoice_line import AccountInvoiceLine


class SaleInvoiceLine(AccountInvoiceLine):
    """Represents a sale invoice's line."""

    def __init__(self, invoice_id, product, qty):
        super().__init__(invoice_id, product, qty)
