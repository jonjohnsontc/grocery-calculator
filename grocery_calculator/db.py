import os
import duckdb

from typing import List, Any, Optional, Union

from grocery_calculator.logger import setup_logger


class Database:

    def __init__(self, conn_str=None):
        self.conn_str = conn_str
        self.logger = setup_logger(self.__class__.__name__)

    def connect(self) -> None:
        if self.conn_str:
            if not os.path.exists(self.conn_str):
                self.logger.info(
                    "Path does not exist %s, so connect may not work if intermediate folders are not created",
                    self.conn_str,
                )
            self.con = duckdb.connect(self.conn_str)
        else:
            self.con = duckdb.connect(":memory:")

    def execute_query(
        self, text: str, params: Optional[Union[dict, list]] = None
    ) -> Optional[List[Any]]:
        self._validate()

        self.logger.info("Executing query %s", text.replace("\n", " "))
        if params:
            self.logger.info("With params %s", params)

        res: Union[duckdb.DuckDBPyRelation, duckdb.DuckDBPyConnection]
        if not params:
            res = self.con.sql(text)
        else:
            res = self.con.execute(text, parameters=params)

        if not res:
            return None
        return res.fetchall()

    def execute_many(self, text: str, params: list) -> Optional[List[Any]]:
        self._validate()
        res: Union[duckdb.DuckDBPyRelation, duckdb.DuckDBPyConnection]
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
