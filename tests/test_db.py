import unittest

from grocery_calculator.db import Database


class TestDB(unittest.TestCase):

    def test_connect_connects_to_database(self):
        db = Database()
        db.connect(test=True)

        self.assertIsNotNone(db.con)

    def test_execute_query_submits_sql_and_returns_result(self):
        db = Database()
        db.connect(test=True)

        actual = db.execute_query("SELECT 42")

        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0][0], 42)

    def test_update_executes_dml_against_store(self):
        db = Database()
        db.connect(test=True)

        db.update("create table test (id INTEGER, val TEXT)")
        db.update("insert into test (id, val) VALUES (12, 'hawk')")
        actual = db.execute_query("select * from test")

        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0][0], 12)
        self.assertEqual(actual[0][1], "hawk")
