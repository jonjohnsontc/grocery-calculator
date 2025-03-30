from contextlib import contextmanager
from pathlib import Path

import logging

FIXTURES_DIR = Path(__file__).parent.joinpath("fixtures").as_posix()


@contextmanager
def suppress_logging():
    logging.disable(logging.CRITICAL)
    try:
        yield
    finally:
        logging.disable(logging.NOTSET)
