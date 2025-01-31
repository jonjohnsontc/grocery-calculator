import duckdb

from typing import List, Any, Optional, Union


class Database:

    def __init__(self, conn_str=None):
        self.conn_str = conn_str

    def connect(self) -> None:
        if self.conn_str:
            self.con = duckdb.connect(self.conn_str)
        else:
            self.con = duckdb.connect(":memory:")

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

    def execute_many(self, text: str, params=None) -> Optional[List[Any]]:
        self._validate()
        res: Union[duckdb.DuckDBPyRelation, duckdb.DuckDBPyConnection]
        if not params:
            res = self.con.executemany(text)
        else:
            res = self.con.executemany(text, parameters=params)

        if not res:
            return None
        return res.fetchall()

    def _validate(self) -> None:
        """Indicate whether db has a valid connection"""
        if not self.con:
            raise ConnectionError(
                "Not yet connected to database. Have you tried running 'connect'?"
            )
