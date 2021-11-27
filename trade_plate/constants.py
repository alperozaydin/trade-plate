import json
from pathlib import Path


class _Constants:
    OKGREEN = "\033[92m"
    NOTOKRED = "\033[91m"

    CACHE_PATH = Path("/tmp/trade_plate")
    ORDER_BOOK = Path.home() / "Documents/binance_orders.txt"

    def __init__(self):
        self._parity_infos = None

    @property
    def CACHE(self):
        if not self._parity_infos:
            with open(self.CACHE_PATH, "r") as f:
                self._parity_infos = json.loads(f.read())
        return self._parity_infos


Constants: _Constants = _Constants()
