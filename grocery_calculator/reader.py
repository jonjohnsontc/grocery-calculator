"""
Utilities for reading in data or queries
"""


class Reader:
    raw: str
    queries: list

    def __init__(self, path: str):
        self.queries = []

        if not path.endswith(".sql"):
            raise ValueError(f"path expected to end in .sql, path is {path}")
        with open(path, "r") as f:
            self.raw = f.read()

        self.queries = self.raw.split(";")

    @property
    def num_queries(self) -> int:
        return len(self.queries)


def read_sql(path) -> str:
    if not path.endswith(".sql"):
        raise ValueError(f"path expected to end in .sql, path is {path}")
    with open(path, "r") as f:
        return f.read()
