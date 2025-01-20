import os
import unittest
import logging

from grocery_calculator.env import load_env_file
from tests import FIXTURES_DIR


FILE = f"{FIXTURES_DIR}/test.env"


class TestEnv(unittest.TestCase):

    def setUp(self):
        self.original_env = os.environ.copy()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_load_env_file_loads_all_vars(self):
        load_env_file(FILE)
        self.assertIn("KEY1", os.environ)
        self.assertIn("ALREADY_EXISTS", os.environ)

    def test_load_env_doesnt_overwrite_already_set_vars(self):
        os.environ["ALREADY_EXISTS"] = "now_set"

        # we want to surpress any warnings from the logger
        logger = logging.getLogger()
        prev_level = logger.level
        logger.setLevel(logging.ERROR)

        try:
            load_env_file(FILE)
        finally:
            logger.setLevel(prev_level)

        self.assertEqual(os.environ.get("ALREADY_EXISTS"), "now_set")
