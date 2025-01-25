"""
Utilities for reading in data or queries
"""


class Reader:
    """
    Reads queries into a named mapping of queries to strings of query text, similar
    to libraries like aiosql.
    """

    raw: str
    mapping: dict

    def __init__(self, path: str):
        if not path.endswith(".sql"):
            raise ValueError(f"path expected to end in .sql, path is {path}")
        with open(path, "r") as f:
            self.raw = f.read()

        self.mapping = {}
        self._parse_queries(self.raw)

    def _parse_queries(self, text: str):
        queries = text.split(";")
        queries = [s.strip() for s in queries]

        for query in queries:
            if not query:
                continue

            split = query.splitlines()

            # we should first see the query has a name
            # and an optional description
            if not (split[0].startswith("--") and "name" in split[0]):
                raise ValueError("Each query in a file should be named")

            qname = _parse_name(split[0])
            qtext = ""
            for line in split[1:]:
                if not line.startswith("--"):
                    qtext += line
                    qtext += "\n"
            qtext = qtext.strip()

            setattr(self, qname, qtext)
            self.mapping[qname] = getattr(self, qname)


def _parse_name(text: str) -> str:
    """Take text identifying the name of a query into its name"""
    name = text.split("name:", maxsplit=1)[-1]
    return name.lower().strip().replace("-", "_")


def read_sql(path) -> str:
    if not path.endswith(".sql"):
        raise ValueError(f"path expected to end in .sql, path is {path}")
    with open(path, "r") as f:
        return f.read()
