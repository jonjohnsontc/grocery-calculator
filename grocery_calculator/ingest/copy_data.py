"""
Script to copy raw data from directory to preprocessing store
"""

import argparse
import os
import subprocess

from pathlib import Path

from grocery_calculator.env import get_project_details, SOURCES
from grocery_calculator.ingest.stores.target import TargetIngest
from grocery_calculator.ingest import INGEST_SQL_FOLDER

DB = os.getenv("DB_CONN_STR")


def get_parser() -> argparse.ArgumentParser:
    source_names = SOURCES
    proj_name = get_project_details()["project"]["name"]
    parser = argparse.ArgumentParser(
        prog=f"{proj_name} - copy data", description=__doc__
    )
    parser.add_argument(
        "--store",
        "-s",
        required=True,
        help=f"Name of store, currently {source_names} are valid",
    )
    parser.add_argument(
        "--folder", "-f", required=True, help="folder where raw data is stored"
    )
    parser.add_argument(
        "--db", required=False, help="location of database file", default=DB
    )
    return parser


def copy_raw_data(store: str, directory: Path, db: str) -> None:
    if store not in SOURCES:
        print("Valid store sources are %s, you passed %s", SOURCES, store)
        SystemExit(1)
    elif store in ["ralphs", "trader_joes"]:
        print("Not yet implemented")
        SystemExit(1)
    elif store == "target":
        ti_script = INGEST_SQL_FOLDER.joinpath("copy_target_2.sql")
        subprocess.run(
            f"cat {ti_script} | duckdb {db}", shell=True, stderr=subprocess.STDOUT
        )
    return


def main():
    parser = get_parser()
    args = parser.parse_args()
    copy_raw_data(args.store, args.folder, args.db)


if __name__ == "__main__":
    main()
