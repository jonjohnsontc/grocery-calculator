import unittest

from grocery_calculator.db import Database
from grocery_calculator.model.seed import seed_db
from tests import suppress_logging


class TestSeed(unittest.TestCase):

    def test_seed_creates_all_tables(self):
        db = Database()
        db.connect()

        with suppress_logging():
            seed_db(db)

            actual = db.execute_query(
                "SELECT list(table_name) FROM (SELECT distinct table_name AS table_name FROM information_schema.columns)",
            )
        actual_table_names = actual[0][0]
        expected_table_names = [
            "categories",
            "products",
            "product_tags",
            "store_locations",
            "store_selection",
            "coupons",
            "store_coupon_policies",
            "price_history",
            "ingest_meta",
        ]

        expected_table_count = 10
        self.assertEqual(len(actual_table_names), expected_table_count)
        for name in expected_table_names:
            self.assertIn(name, actual_table_names)
