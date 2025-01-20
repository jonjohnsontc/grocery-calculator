import os
import unittest

from pathlib import Path

from grocery_calculator.env import load_env_file


class TestEnv(unittest.TestCase):

    FILE = Path(__file__).parent.joinpath("fixtures", "test.env").as_posix()

    def setUp(self):
        self.original_env = os.environ.copy()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_load_env_file_loads_all_vars(self):
        load_env_file(self.FILE)
        self.assertIn("KEY1", os.environ)
        self.assertIn("ALREADY_EXISTS", os.environ)

    def test_load_env_doesnt_overwrite_already_set_vars(self):
        os.environ["ALREADY_EXISTS"] = "now_set"
        load_env_file(self.FILE)
        self.assertEqual(os.environ.get("ALREADY_EXISTS"), "now_set")
