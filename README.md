## Very Basic Invoice Model Example

	program: Very Basic Invoice Model Example.
	version: 0.0.1
	author: Joan A. Pinol
	author_nickname: japinol
	author_gitHub: japinol7
	author_twitter: @japinol
	description: Very Basic Invoice Model example.
	Python requires: 3.8 or greater.
	Python versions tested: 
        > 3.8.5   64bits under Windows 10
        > 3.9.12  64bits under Windows 10


**How to test the implementation**

	Do this:
	    1. Clone this repository in your local system.
	    2. Go to its folder in your system.
	    3. $ python -m unittest

    This should result in some logs and it should end this way:
	    …
        Ran 18 tests in 0.006s
        OK


**Requirements**

    1. Code a model for an invoice that:
        • Store the following information:
            • The quantity sold for each product
            • The total amount of the invoice
            • The client information
            • The company information.
        • Simulate storing this information into a database.
    2. Write unit tests using unittest to test the implementation.
    3. The implementation will use Python 3.8.


**Analysis**

    • I decided to structure the project in five main module-packages (add-ons): 
          base, account, contacts, product and sale.
    • Each main module-package (add-on) will have two packages: models and tests.
    • The main module account will implement the classes AccountInvoice and AccountInvoiceLine.
    • The main module base will create a dummy class DBDriver to connect and write to a fictional database.
    • The main module sale will implement the classes SaleInvoice and SaleInvoiceLine.
    • They will be subclasses of AccountInvoice and AccountInvoiceLine from the account module .
    • The main tests are in the main module account, inside test_account_invoice.py 
      and the main module sale, in test_sale_invoice.py


**In more detail**


    • account
        • models
            • account_invoice.py
              Implements the model account_invoice.
              Classes: AccountInvoice, AccountInvoiceLine, AccountInvoiceType and AccountInvoiceException.
              It’s not intended to be used directly. 
              Instead, its classes are intended to be used through the subclass module sale 
              (and a future module purchase).
        • tests
            • test_account_invoice.py
              Here are the main tests for all the functionality of the invoices.
    • base
        • models
            • db_driver.py
              Implements a dummy model db_driver.
              Classes: DBDriver.
        • tests
            • test_db_driver.py
    • contacts
        • models
            • contact.py
        • tests
            • test_contact.py
    • product
        • models
            • product.py
        • tests
            • test_product.py
    • sale
        • models
            • sale_invoice.py
              Implements the model sale_invoice.
              Classes: SaleInvoice and SaleInvoiceLine .
              These classes inherit AccountInvoice and AccountInvoiceLine from the account module.
              SaleInvoice puts the attribute invoice_type to AccountInvoiceType.OUT 
              and adds the string 'INV/OUT/' to the field invoice_id.
        • tests
            • test_sale_invoice.py
              This module adds some tests for the characteristics added to sale invoices.
              Although, the main tests for invoices are in the module test_account_invoice.py.
