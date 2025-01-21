"""
Seed the application database with data model
"""

from pathlib import Path

from grocery_calculator.db import Database
from grocery_calculator.env import load_env_file
from grocery_calculator.reader import read_sql

SEED_QUERY_LOCATION = Path(__file__).parents[1].joinpath("sql", "seed.sql").as_posix()
ENV_FILE = Path(__file__).parents[1].joinpath(".env").as_posix()


def seed_db(db: Database) -> None:
    db.update(read_sql(SEED_QUERY_LOCATION))


if __name__ == "__main__":
    load_env_file(ENV_FILE)
    db = Database()
    db.connect()
    seed_db(db)
