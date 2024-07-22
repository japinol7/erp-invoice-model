"""Module product.
Implements the model product.
Depends on:
"""


class Product:
    """Represents a product."""

    def __init__(self, name, price, description=None):
        self.name = name
        self.description = description or ""
        self.price = price
