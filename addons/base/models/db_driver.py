"""Module db_driver.
Implements the model db_driver.
Coding: utf-8
Author: 'Joan A. Pinol  (japinol)'
Depends on:
"""

from tools.logger.logger import log as logger


class DBDriver:
    """Represents a database driver."""

    def __init__(self):
        self.name = 'dummy_db'

        self.connect()

    def connect(self):
        logger.info(f"Connecting database {self.name}.")

    def write(self, table, vals):
        for k, v in vals.items():
            logger.info(f"Writing field to db table {table}: {k} -> {v}")

    def insert(self, table, vals):
        for k, v in vals.items():
            logger.info(f"Insert field to db table {table}: {k} -> {v}")

    def update(self, table, vals):
        for k, v in vals.items():
            logger.info(f"Update field to db table {table}: {k} -> {v}")


db_driver = DBDriver()
