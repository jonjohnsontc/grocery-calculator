from os import getenv
from typing import List, Tuple, Generator

from grocery_calculator.logging import setup_logger
from grocery_calculator.ingest import Ingest, INGEST_SQL_FOLDER
from grocery_calculator.reader import read_sql, Reader
from grocery_calculator.ingest.llm_tagger import tag_item

DB_CONN_STR = getenv("DB_CONN_STR")
TAGGING_CHUNK_SIZE = 10


class TargetIngest(Ingest):
    def __init__(self, conn_str=None):
        super().__init__(conn_str)
        self._tag_item = tag_item

    def copy_data(self, location):
        ingest_query = read_sql(f"{INGEST_SQL_FOLDER}/copy_target.sql")
        result = self.db.execute_query(ingest_query, location)
        num_rows = result[0][0]
        return num_rows

    def preprocess(self):
        reader = Reader(f"{INGEST_SQL_FOLDER}/preprocess_target.sql")
        data = self.db.execute_query(reader.get_target_detail)
        for tagged_items in self.tag_items(data, chunk_size=TAGGING_CHUNK_SIZE):
            self.db.execute_many(reader.copy_tagged_data, tagged_items)
            # TODO: I want to log here -> copied TAGGING_CHUNK_SIZE items to table
        return

    def update(self):
        return

    def tag_items(
        self, items: List[Tuple[int, str]], chunk_size=20
    ) -> Generator[List[tuple]]:
        tagged = []
        for item_idx, item_descr in items:
            try:
                res = self._tag_item(item_descr)
                tagged.append((item_idx, *res))
            except Exception as e:  # should get more specific
                # should log the error here
                continue

            if len(tagged) == chunk_size:
                yield tagged.copy()
                tagged = []

        if tagged:
            yield tagged.copy()


def ingest_target_v0(location: str) -> None:
    pass


if __name__ == "__main__":
    pass
