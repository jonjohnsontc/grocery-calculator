import unittest

from grocery_calculator.db import Database
from grocery_calculator.model.seed import seed_db


class TestSeed(unittest.TestCase):

    def test_seed_creates_all_tables(self):
        db = Database()
        db.connect(test=True)

        seed_db(db)

        actual = db.execute_query(
            "SELECT distinct table_name FROM information_schema.columns"
        )

        expected_table_count = 10
        self.assertEqual(len(actual), expected_table_count)
