import unittest
from pathlib import Path

from grocery_calculator.reader import read_sql

FIXTURES_DIR = Path(__file__).parent.joinpath("fixtures")


class TestReader(unittest.TestCase):

    def test_read_sql_reads_sql_file_successfully(self):
        test_sql_file = FIXTURES_DIR.joinpath("hello.sql").as_posix()
        actual = read_sql(test_sql_file)
        expected = "SELECT 'hello world';"
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
