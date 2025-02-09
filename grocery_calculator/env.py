"""
Supports dynamically loading in staic environment variables, and generating 
other runtime environment variables
"""

import os
import logging
import tomllib

PYPROJECT_FILE = "pyproject.toml"
SOURCES = ["trader_joes", "target", "ralphs"]


def get_project_details() -> dict:
    with open(PYPROJECT_FILE, "rb") as f:
        return tomllib.load(f)


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
