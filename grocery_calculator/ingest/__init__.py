from abc import ABC


class Ingest(ABC):
    """
    Designed to be a thin wrapper around some SQL executed in a database
    """

    def copy_data(self, location: str) -> None:
        pass

    def validate(self) -> None:
        pass

    def normalize(self) -> None:
        pass
