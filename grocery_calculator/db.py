import os
import duckdb

from typing import List, Any

CONN_STR = os.getenv("DB_CONN_STR")


class Database:

    def connect(self) -> None:
        if not CONN_STR:
            raise OSError("Database connection string 'DB_CONN_STR' not found")
        self.con = duckdb.connect(CONN_STR)

    def execute_query(self, text: str) -> List[Any]:
        if not self.con:
            raise ConnectionError(
                "Not yet connected to database. Have you tried running 'connect'?"
            )
        return self.con.sql(text).fetchall()
