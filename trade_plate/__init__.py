"""Top-level package for Trade Plate."""

__author__ = """Alper Ozaydin"""
__email__ = "alperozaydinn@gmail.com"
__version__ = "0.1.0"

from pathlib import Path

from trade_plate.constants import Constants


def init_cache() -> None:
    if not Path(Constants.CACHE_PATH).exists():
        with open(Constants.CACHE_PATH, "w") as f:
            f.write("{}")


init_cache()
