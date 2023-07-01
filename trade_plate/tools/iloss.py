import json
from typing import Tuple

import requests
from pycoingecko import CoinGeckoAPI

from trade_plate.tools.constants import DeBankAPI, WALLETS


class Iloss:
    def __init__(
        self,
        protocol_id: str,
        pool_id: str,
        asset_price_1: Tuple[str, float],
        asset_price_2: Tuple[str, float],
        cost: float = 1000,
    ):
        self.cg = CoinGeckoAPI()
        self.protocol_id = protocol_id
        self.pool_id = pool_id
        self.cost = cost
        self.asset1, self.price1 = asset_price_1
        self.asset1_amount = self.cost / 2 / self.price1
        self.asset1_current_price = self._get_current_price(self.asset1)

        self.asset2, self.price2 = asset_price_2
        self.asset2_amount = self.cost / 2 / self.price2
        self.asset2_current_price = self._get_current_price(self.asset2)

        self.session = requests.session()

    def _get_current_price(self, asset) -> float:
        return self.cg.get_price(ids=asset, vs_currencies="usd")[asset]["usd"]

    @staticmethod
    def _iloss(price_ratio) -> float:
        return 2 * (price_ratio ** 0.5 / (1 + price_ratio)) - 1

    def run(self) -> None:
        iloss = self._iloss(self._price_ratio())
        hodl_value = self._hodl_value()
        print(
            f"Asset: {self.asset1}/{self.asset2}\n"
            f"Impermanent loss: {iloss:.2%}\n"
            f"Invested: ${self.cost}\n"
            f"HODL value: ${round(hodl_value, 2)}\n"
            f"LP value wout rewards: ${round(hodl_value * iloss + hodl_value, 2)}\n"
            f"LP value with rewards: ${round(self._real_value(), 2)}\n"
            f"Profit/Loss: {round(self.profit_or_loss(), 2)}$\n"
            f"------------------------------"
        )

    def _variation(self, asset, price) -> float:
        current_price1 = self._get_current_price(asset=asset)
        var1 = ((current_price1 / price) - 1) * 100
        return var1

    def _price_ratio(self) -> float:
        return (self._variation(self.asset1, self.price1) / 100 + 1) / (
            self._variation(self.asset2, self.price2) / 100 + 1
        )

    def _hodl_value(self) -> float:
        return (
            self.asset1_amount * self.asset1_current_price
            + self.asset2_amount * self.asset2_current_price
        )

    #  Remove debank API because there is no free version anymore
    def _real_value(self) -> float:
        with self.session.get(
            DeBankAPI.PROTOCOL_URL,
            headers={DeBankAPI.ACCESS_KEY},
            params={"protocol_id": self.protocol_id, "id": WALLETS.EVM_WALLET},
        ) as r:
            if r.ok:
                portfolios = json.loads(r.content)
            else:
                raise r.content

        for portfolio in portfolios.get("portfolio_item_list"):
            if portfolio.get("pool").get("id") == self.pool_id:
                return portfolio.get("stats").get("asset_usd_value")

    def profit_or_loss(self):
        return self._real_value() - self.cost
