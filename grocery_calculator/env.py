import os
import logging


def load_env_file(path: str) -> None:
    with open(path, "r") as f:
        for ln in f:
            ln = ln.strip()
            key, value = ln.split("=", 1)

            if os.environ.get(key):
                logging.warning(
                    f"{key} would overwrite already set environment variable; skipping"
                )
                continue
            os.environ[key] = value
