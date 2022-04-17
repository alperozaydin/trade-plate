import json

import requests
from pycoingecko import CoinGeckoAPI

from trade_plate.tools.constants import PARAS, GENERAL


class Paras:
    def __init__(self, collection_id):
        self.collection_id = collection_id
        self.session = requests.session()
        with self.session.get(
            PARAS.COLLECTION_STATS,
            params={"collection_id": collection_id},
        ) as r:
            self.collection_stats = json.loads(r.content)
        self.collection_data = self.collection_stats.get("data").get("results")
        self.collection_fp = None
        self.token_data = None
        self._collection_value = None
        self.cg = CoinGeckoAPI()

    @property
    def floor_price(self):
        self.collection_fp = self.collection_data.get("floor_price")
        assert self.collection_fp, "Floor price cannot be None"
        return int(self.collection_fp) / 1e24

    def _get_nft_data_by_owner(self):
        with self.session.get(
            PARAS.COLLECTION_TOKEN,
            params={
                "collection_id": self.collection_id,
                "owner_id": GENERAL.NEAR_WALLET,
                "__limit": "1000",
            },
        ) as r:
            self.token_data = json.loads(r.content)

    def get_nft_amount_by_owner(self):
        if not self.token_data:
            self._get_nft_data_by_owner()
        return len(self.token_data.get("data").get("results"))

    @property
    def collection_value(self):
        if not self._collection_value:
            self._collection_value = round(
                self.get_nft_amount_by_owner() * self.floor_price, 3
            )
        return self._collection_value

    def get_near_price(self):
        return self.cg.get_price(ids="near", vs_currencies="usd")["near"]["usd"]

    def show_results(self):
        print(
            f"Collection: {self.collection_id}\n"
            f"Floor Price: {round(self.floor_price, 2)} N\n"
            f"Total Value Based on FP: {self.collection_value} N "
            f"(${round(self.get_near_price() * self.collection_value, 2)})\n"
            f"------------------------------"
        )
