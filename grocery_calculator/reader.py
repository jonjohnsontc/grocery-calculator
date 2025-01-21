"""
Utilities for reading in data or queries
"""


def read_sql(path) -> str:
    if not path.endswith(".sql"):
        raise ValueError(f"path expected to end in .sql, path is {path}")
    with open(path, "r") as f:
        return f.read()
