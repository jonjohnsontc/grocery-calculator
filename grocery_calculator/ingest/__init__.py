from abc import ABC


class Ingest(ABC):
    """
    Designed to be a thin wrapper around some SQL executed in a database
    """

    def copy_data(self, location: str) -> None:
        pass

    def preprocess(self) -> dict:
        pass

    def update(self, data) -> None:
        pass


class TargetIngest(Ingest):
    pass


class TraderJoesIngest(Ingest):
    pass
