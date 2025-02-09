"""
Preprocess raw data from stores into valid format for solving shopping trips 
"""

import argparse
import os

from grocery_calculator.env import get_project_details, SOURCES
from grocery_calculator.ingest.stores.target import TargetIngest

DB = os.getenv("DB_CONN_STR")
proj_name = get_project_details()["project"]["name"]


def get_parser() -> argparse.ArgumentParser:
    source_names = SOURCES
    parser = argparse.ArgumentParser(
        prog=f"{proj_name} - preprocess", description=__doc__
    )
    parser.add_argument(
        "--store",
        "-s",
        required=True,
        help=f"Name of store, currently {source_names} are valid",
    )
    parser.add_argument(
        "--db", required=False, help="location of database file", default=DB
    )
    return parser


def preprocess_data(store: str, db: str) -> None:
    if store not in SOURCES:
        raise ValueError("Valid store sources are %s, you passed %s", SOURCES, store)
    elif store in ["ralphs", "trader_joes"]:
        raise NotImplementedError("Not yet implemented")
    elif store == "target":
        ti = TargetIngest(db)
        ti.preprocess()
    pass


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    preprocess_data(args.store, args.db)
