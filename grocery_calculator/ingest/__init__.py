from abc import ABC
from os import getenv
from pathlib import Path

from grocery_calculator.db import Database
from grocery_calculator.reader import read_sql

CONN_STR = getenv("CONN_STR")
INGEST_SQL_FOLDER = Path(__file__).parent.joinpath("sql", "ingest")


class Ingest(ABC):
    """
    Designed to be a thin wrapper around some SQL executed in a database
    """

    def __init__(self, conn_str=None):
        self.db = Database(conn_str)
        self.db.connect()

    def copy_data(self, location: str) -> None:
        pass

    def preprocess(self) -> dict:
        pass

    def update(self) -> None:
        pass
