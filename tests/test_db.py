import unittest

from grocery_calculator.db import Database


class TestDB(unittest.TestCase):

    def test_connect_connects_to_database(self):
        db = Database()
        db.connect(test=True)

        self.assertIsNotNone(db.con)
