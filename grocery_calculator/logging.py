import logging
import sys


def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    Setup and return logging stream handler for stdout
    """

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger
