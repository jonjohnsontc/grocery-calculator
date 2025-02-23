import json

from os import getenv
from typing import List, Tuple

from grocery_calculator.ingest import Ingest, INGEST_SQL_FOLDER
from grocery_calculator.reader import read_sql, Reader
from grocery_calculator.ingest.llm_tagger import tag_item

DB_CONN_STR = getenv("DB_CONN_STR")
TAGGING_CHUNK_SIZE = 5


def chunk(lst: list, chunksize: int):
    for i in range(0, len(lst), chunksize):
        yield lst[i : i + chunksize]


class TargetIngest(Ingest):
    def __init__(self, conn_str=None):
        super().__init__(conn_str)
        self._tag_item = tag_item

    def copy_data(self, location):
        ingest_query = read_sql(f"{INGEST_SQL_FOLDER}/copy_target_2.sql")
        result = self.db.execute_query(ingest_query, location)
        num_rows = result[0][0]
        return num_rows

    def preprocess(self):
        reader = Reader(f"{INGEST_SQL_FOLDER}/preprocess_target.sql")
        data = self.db.execute_query(reader.get_target_detail)
        rows_tagged = 0

        for items in chunk(data, TAGGING_CHUNK_SIZE):
            tagged_items = self.tag_items(items)
            try:
                self.db.execute_many(reader.copy_tagged_data, tagged_items)
            except Exception as e:
                self.logger.error("exception encountered %s", e)
                self.logger.error("tagged items contents %s", tagged_items)
                raise e

            rows_tagged += len(tagged_items)
            self.logger.info("%d rows tagged for target", rows_tagged)
        return

    def update(self):
        return

    # TODO: This functionality should be in llm_tagger
    def tag_items(self, items: List[Tuple[int, str]]) -> List[tuple]:
        tagged = []
        for item_idx, item_descr in items:
            self.logger.info("item_idx %d", item_idx)
            self.logger.info("item descr %s", item_descr)
            try:
                res = self._tag_item(item_descr)
            except json.JSONDecodeError:
                self.logger.error(
                    "LLM Submitted invalid JSON response for item_idx %s", item_idx
                )
                continue

            self.logger.info("Item tagged info %s", res)
            tagged.append(
                (
                    item_idx,
                    res["product_name"],
                    res["product_type"],
                    res["flavor_or_variant"],
                    res["size"],
                    res["packaging_type"],
                    res["sale"],
                    res["sale_value"],
                    res["tags"],
                )
            )

        return tagged
