from typing import Tuple

from pycoingecko import CoinGeckoAPI


class Iloss:
    def __init__(
        self,
        asset_price_1: Tuple[str, float],
        asset_price_2: Tuple[str, float],
        cost: float = 1000,
    ):
        self.cg = CoinGeckoAPI()
        self.cost = cost
        self.asset1, self.price1 = asset_price_1
        self.asset1_amount = self.cost / 2 / self.price1
        self.asset1_current_price = self._get_current_price(self.asset1)

        self.asset2, self.price2 = asset_price_2
        self.asset2_amount = self.cost / 2 / self.price2
        self.asset2_current_price = self._get_current_price(self.asset2)

    def _get_current_price(self, asset) -> float:
        return self.cg.get_price(ids=asset, vs_currencies="usd")[asset]["usd"]

    @staticmethod
    def iloss(price_ratio) -> float:
        return 2 * (price_ratio ** 0.5 / (1 + price_ratio)) - 1

    def run(self) -> None:
        iloss = self.iloss(self._price_ratio())
        hodl_value = self._hodl_value()
        print(
            f"Asset: {self.asset1}/{self.asset2}\n"
            f"Impermanent loss: {iloss:.2%}\n"
            f"Invested: ${self.cost}\n"
            f"HODL: ${round(hodl_value, 2)}\n"
            f"LP: ${round(hodl_value * iloss + hodl_value, 2)}\n"
            f"Profit/Loss: {round(self.profit_or_loss(), 2)}$\n"
            f"------------------------------"
        )

    def _variation(self, asset, price) -> float:
        current_price1 = self.cg.get_price(ids=asset, vs_currencies="usd")[asset]["usd"]
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

    def profit_or_loss(self):
        return self._hodl_value() - self.cost
