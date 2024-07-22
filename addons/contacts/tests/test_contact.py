"""Tests model contact.
Coding: utf-8
Author: 'Joan A. Pinol  (japinol)'
"""

__author__ = "Joan A. Pinol  (japinol)"

import unittest

from addons.contacts.models.contact import Contact


class TestAccountInvoice(unittest.TestCase):
    def test_create_contact(self):
        """Tests the creation of a contact."""
        contact = Contact(
            "Company_assignment", "info@company_assignment.com", vat="89735694-U"
        )

        self.assertEqual(contact.name, "Company_assignment")
        self.assertEqual(contact.email, "info@company_assignment.com")
        self.assertEqual(contact.props.get("vat"), "89735694-U")


if __name__ == "__main__":
    unittest.main()
