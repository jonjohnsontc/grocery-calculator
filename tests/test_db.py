import unittest

from grocery_calculator.db import Database

from tests import FIXTURES_DIR

TEST_FILE_DB = f"{FIXTURES_DIR}/test.db"


class TestDB(unittest.TestCase):

    def test_connect_connects_to_database(self):
        db = Database()
        db.connect()

        self.assertIsNotNone(db.con)

    def test_connect_with_query_string_connects_to_file_db(self):
        db = Database(TEST_FILE_DB)
        db.connect()

        actual = db.execute_query("pragma database_list")
        # file column should be a string pointing to the correct file
        self.assertIsNotNone(actual[0][2])

    def test_connect_without_query_string_connects_to_in_memory_db(self):
        db = Database()
        db.connect()
        actual = db.execute_query("pragma database_list")

        # file column in database_list will be None
        self.assertIsNone(actual[0][2])

    def test_execute_query_submits_sql_and_returns_result(self):
        db = Database()
        db.connect()

        actual = db.execute_query("SELECT 42")

        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0][0], 42)

    def test_execute_query_executes_dml_against_store(self):
        db = Database()
        db.connect()

        db.execute_query("create table test (id INTEGER, val TEXT)")
        db.execute_query("insert into test (id, val) VALUES (12, 'hawk')")
        actual = db.execute_query("select * from test")

        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0][0], 12)
        self.assertEqual(actual[0][1], "hawk")

    def test_execute_many_executes_all_bound_stmts_against_store(self):
        db = Database()
        db.connect()

        db.execute_query("create table test (id INTEGER, val TEXT)")
        db.execute_many(
            "insert into test (id, val) VALUES (?, ?)",
            [(12, "hawk"), (18, "ferdinand"), (2, "aj hawk")],
        )
        actual = db.execute_query("select * from test order by id")

        self.assertEqual(len(actual), 3)
        self.assertEqual(actual[0][0], 2)
        self.assertEqual(actual[2][1], "ferdinand")
