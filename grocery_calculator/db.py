import os
import duckdb

from typing import List, Any, Optional, Union

CONN_STR = os.getenv("DB_CONN_STR")


class Database:

    def connect(self, test=False) -> None:
        if not CONN_STR and not test:
            raise OSError("Database connection string 'DB_CONN_STR' not found")
        elif test:
            self.con = duckdb.connect()
        else:
            self.con = duckdb.connect(CONN_STR)

    def execute_query(self, text: str, params=None) -> Optional[List[Any]]:
        self._validate()
        res: Union[duckdb.DuckDBPyRelation, duckdb.DuckDBPyConnection]
        if not params:
            res = self.con.sql(text)
        else:
            res = self.con.execute(text, parameters=params)

        if not res:
            return None
        return res.fetchall()

    def _validate(self) -> None:
        """Indicate whether db has a valid connection"""
        if not self.con:
            raise ConnectionError(
                "Not yet connected to database. Have you tried running 'connect'?"
            )
