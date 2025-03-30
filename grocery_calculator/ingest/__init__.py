from abc import ABC
from os import getenv
from pathlib import Path

from grocery_calculator.db import Database
from grocery_calculator.logger import setup_logger

CONN_STR = getenv("CONN_STR")
INGEST_SQL_FOLDER = Path(__file__).parents[1].joinpath("sql", "ingest")


class Ingest(ABC):
    """
    Designed to be a thin wrapper around some SQL executed in a database
    """

    def __init__(self, conn_str=None):
        self.db = Database(conn_str)
        self.db.connect()
        self.logger = setup_logger(self.__module__)

    def copy_data(self, location: str) -> None:
        """Copy raw data to store for preprocessing and return number of rows copied"""
        pass

    def preprocess(self) -> dict:
        pass

    def update(self) -> None:
        pass
