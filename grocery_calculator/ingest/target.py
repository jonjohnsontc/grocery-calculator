from os import getenv
from typing import List, Tuple

from ingest import Ingest, INGEST_SQL_FOLDER
from reader import read_sql, Reader


DB_CONN_STR = getenv("DB_CONN_STR")


class TargetIngest(Ingest):
    def __init__(self, conn_str=None):
        super().__init__(conn_str)

    def copy_data(self, location):
        ingest_query = read_sql(f"{INGEST_SQL_FOLDER}/copy_target.sql")
        result = self.db.execute_query(ingest_query, location)
        num_rows = result[0][0]
        return num_rows

    def preprocess(self):
        data = self.db.execute_query()

        return

    def update(self):
        return

    def tag_items(
        self, items: List[Tuple[int, str]], chunk_size=20
    ) -> List[Tuple[int, str]]:
        pass


def ingest_target_v0(location: str) -> None:
    pass


if __name__ == "__main__":
    pass
