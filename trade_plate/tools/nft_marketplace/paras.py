import json
import logging

import requests
from pycoingecko import CoinGeckoAPI

from trade_plate.tools.constants import PARAS, WALLETS

LOG = logging.getLogger()


class Paras:
    def __init__(self, collection_id):
        self._collection_id = collection_id
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
    def collection_id(self):
        return self._collection_id

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
                "owner_id": WALLETS.NEAR_WALLET,
                "__limit": "1000",
            },
        ) as r:
            self.token_data = json.loads(r.content)

    @property
    def holding_amount(self):
        if not self.token_data:
            self._get_nft_data_by_owner()
        return len(self.token_data.get("data").get("results"))

    @property
    def collection_value(self):
        if not self._collection_value:
            self._collection_value = round(self.holding_amount * self.floor_price, 3)
        return self._collection_value

    def get_near_price(self):
        return self.cg.get_price(ids="near", vs_currencies="usd")["near"]["usd"]

    def get_offers_collection(self):
        results = []
        total_cards = self.collection_data.get("total_cards")
        for i in range(1, total_cards):
            if i % 25 == 0:
                LOG.info(f"Fetching offers for {self.collection_id}: {i}/{total_cards}")
            with self.session.get(
                PARAS.COLLECTION_OFFERS,
                params={
                    "token_id": str(i),
                    "contract_id": self.collection_id,
                },
            ) as r:
                data = json.loads(r.content).get("data")
                if data.get("results"):
                    results.append(data.get("results"))
        return results
