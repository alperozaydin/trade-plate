import json
import logging

import requests
from pycoingecko import CoinGeckoAPI

from trade_plate.tools.constants import PARAS, WALLETS

LOG = logging.getLogger()


class Paras:
    RATE_LIMIT_SECOND = 500

    def __init__(self, collection_id):
        self.collection_id = collection_id
        self.session = requests.session()
        self._collection_data = None
        self._total_cards = None
        self.collection_fp = None
        self.token_data = None
        self._holding_amount = None
        self._collection_value = None
        self.cg = CoinGeckoAPI()

    @property
    def collection_data(self):
        if not self._collection_data:
            with self.session.get(
                PARAS.COLLECTION_STATS,
                params={"collection_id": self.collection_id},
            ) as r:
                self._collection_data = json.loads(r.content).get("data").get("results")
        return self._collection_data

    @property
    def total_cards(self):
        if not self._total_cards:
            self._total_cards = self.collection_data.get("total_cards")
        return self._total_cards

    @property
    def floor_price(self):
        self.collection_fp = self.collection_data.get("floor_price")
        if self.collection_fp:
            return int(self.collection_fp) / 1e24
        return 0

    def _get_nft_data_by_owner(self):
        with self.session.get(
            PARAS.COLLECTION_TOKEN,
            params={
                "collection_id": self.collection_id,
                "owner_id": WALLETS.NEAR_WALLET,
                "__limit": "1000",
            },
        ) as r:
            return json.loads(r.content).get("data").get("results")

    @property
    def holding_amount(self):
        if not self._holding_amount:
            self._holding_amount = len(self._get_nft_data_by_owner())
        return self._holding_amount

    @property
    def collection_value(self):
        if not self._collection_value:
            self._collection_value = round(self.holding_amount * self.floor_price, 3)
        return self._collection_value

    def get_near_price(self):
        return self.cg.get_price(ids="near", vs_currencies="usd")["near"]["usd"]

    def get_offers_collection(self):
        token_ids = self._fetch_token_ids()
        results = []
        for i, id in enumerate(token_ids):
            if i % 100 == 0:
                LOG.info(
                    f"Fetching offers for {self.collection_id}: {i}/{self.total_cards}"
                )
            with self.session.get(
                PARAS.COLLECTION_OFFERS,
                params={
                    "token_id": id,
                    "contract_id": self.collection_id,
                },
            ) as r:
                data = json.loads(r.content).get("data")
                if data.get("results"):
                    results.append(data.get("results"))
        return results

    def _fetch_token_ids(self):
        token_ids = []
        for limit in range(0, self.total_cards, 100):
            LOG.info(
                f"Fetching token ids for {self.collection_id}: "
                f"{limit}/{self.total_cards}"
            )
            with self.session.get(
                PARAS.COLLECTION_TOKEN,
                params={
                    "collection_id": self.collection_id,
                    "__skip": limit,
                    "__limit": 100,
                },
            ) as r:
                tokens = json.loads(r.content).get("data").get("results")
            for token in tokens:
                token_ids.append(token.get("token_id"))
        return token_ids
