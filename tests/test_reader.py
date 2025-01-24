import unittest

from grocery_calculator.reader import read_sql, Reader, _parse_name

from tests import FIXTURES_DIR


class TestReader(unittest.TestCase):

    def test_read_sql_reads_sql_file_successfully(self):
        test_sql_file = f"{FIXTURES_DIR}/hello.sql"
        actual = read_sql(test_sql_file)
        expected = "SELECT 'hello world';"
        self.assertEqual(actual, expected)

    def test_readers_parse_name_parses_name_values_correctly(self):
        test_line_no_space = "--name: query-1"
        test_line_multi_space = "--    name: query-1"
        expected = "query_1"

        self.assertEqual(_parse_name(test_line_no_space), expected)
        self.assertEqual(_parse_name(test_line_multi_space), expected)

    def test_reader_reads_sql_file_into_named_attributes(self):
        test_sql_file = f"{FIXTURES_DIR}/multiple_queries.sql"
        reader = Reader(test_sql_file)

        self.assertTrue(hasattr(reader, "first_query"))
        self.assertTrue(hasattr(reader, "second_query"))

        self.assertEqual(reader.first_query, "SELECT 42 as the_all_important_number")
        self.assertEqual(reader.second_query, "SELECT 27 as the_second_number")


if __name__ == "__main__":
    unittest.main()
