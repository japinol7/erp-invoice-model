"""Module contact.
Implements the model contact.
Depends on:
"""


class Contact:
    """Represents a contact."""

    def __init__(self, name, email, **extra_props):
        self.name = name
        self.email = email
        self.props = {}
        self.props.update(**extra_props)
