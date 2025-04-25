from grocery_calculator.ingest import Ingest, INGEST_SQL_FOLDER
from grocery_calculator.reader import Reader


class TraderJoesIngest(Ingest):

    def __init__(self, conn_str=None):
        super().__init__(conn_str)
        self._tag_item = None

    def copy_data(self, location):
        copy_script = Reader(f"{INGEST_SQL_FOLDER}/copy_trader_joes.sql")
