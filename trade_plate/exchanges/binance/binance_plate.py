import json

import numpy as np
import math
from binance.client import Client
import os
from datetime import datetime, timedelta
from trade_plate.constants import Constants


class Binance:
    MIN_ORDER_AMOUNT = 10.5

    greedy_levels = {
        "1": 2.0,
        "2": 1.9,
        "3": 1.8,
        "4": 1.7,
        "5": 1.5,
        "6": 1.4,
        "7": 1.3,
        "8": 1.2,
    }

    line = "------------------------------------------\n"

    def __init__(self, asset: str, greed: str):
        """
        :param asset: asset symbol with parity e.g. BTCUSDT
        :param greed: 1 to 5
            Greedy level is how eager you are to get that asset. Set it high if
            you prefer to make the purchase of that asset even though the price is
            not that low.
        """
        self.client = Client(
            os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET_KEY")
        )
        self.greedy_level = int(greed)
        self.greed = self.greedy_levels[greed]
        self.asset = asset
        self.parity = "$" if "usdt" in self.asset.lower() else "€"

        self.get_info = self.client.get_symbol_info(self.asset)
        self.step_size = self._get_step_size()
        self.tick_size = self._get_tick_size()

        self.current_price = float(
            self.client.get_avg_price(symbol=self.asset)["price"]
        )
        self.asset_balance = self._get_asset_balance()
        self.my_trades = self.client.get_my_trades(symbol=self.asset)

        print(f"Current Price for {self.asset}: {self.current_price}\n")

    @staticmethod
    def _save_to_file(orders: str) -> None:
        with open(Constants.ORDER_BOOK, "a") as f:
            f.write(orders)

    def _cache_min_max_price(self, max_price: float, min_price: float) -> None:
        with open("/tmp/trade_plate", "r+") as f:
            cache = json.loads(f.read())
            cache[self.asset] = {"min_price": min_price, "max_price": max_price}
            f.seek(0)
            f.write(json.dumps(cache))

    def _get_asset_balance(self) -> tuple:
        asset_balance_info = self.client.get_asset_balance(asset=self._asset_name())
        return float(asset_balance_info["free"]), float(asset_balance_info["locked"])

    def _asset_name(self) -> str:
        if "USDT" in self.asset:
            return self.asset[:-4]
        elif "EUR" in self.asset:
            return self.asset[:-3]
        else:
            raise Exception("Invalid Asset Symbol")

    def _get_step_size(self) -> int:
        if self.get_info is None:
            raise Exception("Invalid Asset parity or something else is wrong")

        for info in self.get_info.get("filters"):
            if info.get("filterType") == "LOT_SIZE":
                return int(round(-math.log(float(info["stepSize"]), 10), 0))

    def _get_tick_size(self) -> int:
        for info in self.get_info.get("filters"):
            if info.get("filterType") == "PRICE_FILTER":
                return int(round(-math.log(float(info.get("tickSize")), 10), 0))

    def create_buy_order(
        self,
        max_price: float,
        min_price: float,
        budget: float,
        make_it=False,
    ) -> int:
        if self.current_price < max_price:
            print(
                "Maximum Buy price is higher than current price. "
                "Check your order again. Exiting..."
            )
            return 1

        bullet = budget / self.MIN_ORDER_AMOUNT
        for i in range(int(bullet), 0, -1):
            cost_range = np.logspace(1.03, self.greed, num=int(i))
            cost = sum(cost_range)
            if cost > (budget + (budget * 0.1)):
                continue
            try:
                price_ranges = np.arange(
                    max_price,
                    min_price,
                    -round(float(max_price - min_price) / (len(cost_range) - 1), 3),
                )
            except ZeroDivisionError:
                print("\nBudget is too low.")
                exit()
            price_ranges = np.append(price_ranges, min_price)

            quantities = list()
            total_cost = list()
            for index, total in enumerate(cost_range):
                quantity = round((float(total) / price_ranges[index]), self.step_size)
                quantities.append(quantity)
                price = price_ranges[index]

                order_time = (
                    f"created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    if make_it
                    else "will be created"
                )
                order_info = (
                    f"BUY Order {order_time}: {self.asset} -> "
                    f"Price: {'%.2f' % round(price, self.tick_size)}, "
                    f"Quantity: {quantity} = {round(total, self.step_size)} "
                    f"{self.parity} "
                )

                total_cost.append(price * quantity)
                print(order_info)

                if make_it:
                    self.client.create_order(
                        symbol=self.asset,
                        side=Client.SIDE_BUY,
                        type=Client.ORDER_TYPE_LIMIT,
                        timeInForce=Client.TIME_IN_FORCE_GTC,
                        quantity=quantity,
                        price=round(price, 3),
                    )

                    self._save_to_file(orders=f"{order_info}\n")

            orders_info = (
                f"\nTotal Cost: {sum(total_cost)} {self.parity}\n"
                f"Trade Average: {sum(total_cost) / sum(quantities)}\n"
                f"Total Qnt: {sum(quantities)}\n"
                f"{self.line}"
            )
            print(orders_info)

            self._cache_min_max_price(max_price=max_price, min_price=min_price)

            if make_it:
                self._save_to_file(orders=orders_info)

            return 0

    def _check_quantity(self, quantity: float):
        available = self.asset_balance[0]
        total = available + self.asset_balance[1]
        print(f"You have Available: {available}, Total: {total} {self._asset_name()}")
        if available < quantity:
            print(
                f"WARNING: You do not have enough {self._asset_name()} "
                f"coin for this order."
            )

    def create_sell_order(self, quantity: float, make_it: bool = False) -> int:
        self._check_quantity(quantity=quantity)
        init_price = self.current_price + (self.current_price / 10)
        unit = round(self.MIN_ORDER_AMOUNT / init_price, self.step_size)
        bullet = quantity / unit

        cost_range = np.logspace(1.03, self.greed, num=int(bullet))
        quantity_range = [unit] * int(bullet)

        for index, cost in enumerate(cost_range):
            unit = quantity_range[index]
            price = cost / unit
            order_time = (
                f"created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                if make_it
                else "will be created"
            )
            orders_info = (
                f"SELL Order {order_time}: {self.asset} -> "
                f"Price: {'%.2f' % round(price, self.tick_size)}, "
                f"Quantity: {unit} = {round(cost, 2)} "
                f"{self.parity} "
            )
            print(orders_info)

            if make_it:
                self.client.create_order(
                    symbol=self.asset,
                    side=Client.SIDE_SELL,
                    type=Client.ORDER_TYPE_LIMIT,
                    timeInForce=Client.TIME_IN_FORCE_GTC,
                    quantity=unit,
                    price=round(price, self.step_size),
                )

                self._save_to_file(orders=f"{orders_info}\n")

        total_cost = sum(cost_range)
        orders_info = (
            f"\nTotal Cost: {total_cost} {self.parity}\n"
            f"Trade Average: {total_cost / quantity}\n"
            f"Total Qnt: {quantity}\n"
            f"{self.line}"
        )
        print(orders_info)

        if make_it:
            self._save_to_file(orders=orders_info)

        return 0

    def trade_summary(self) -> None:
        quoteqty = {"buyer": (list(), list()), "seller": (list(), list())}

        for trade in self.my_trades:
            quoteqty["buyer" if trade["isBuyer"] else "seller"][0].append(
                float(trade["quoteQty"])
            )
            quoteqty["buyer" if trade["isBuyer"] else "seller"][1].append(
                float(trade["qty"])
            )

        buy_cost = sum(quoteqty["buyer"][0])
        sell_cost = sum(quoteqty["seller"][0])

        buy_quantity = sum(quoteqty["buyer"][1])
        sell_quantity = sum(quoteqty["seller"][1])

        worth = sum(self.asset_balance) * self.current_price

        if quoteqty["buyer"] or quoteqty["seller"]:
            try:
                print("Trade summary:")
                print(
                    f"Avg buy price: {buy_cost / buy_quantity}, cost: {buy_cost}, "
                    f"worth: {worth}, P/L: SOON"
                )
                print(
                    f"Ang sell price: {sell_cost / sell_quantity}, cost: {sell_cost}\n"
                )
            except ZeroDivisionError:
                pass
        else:
            print(f"No Trade made for {self.asset}.\n")
        print(self.line)

    def get_summary_range(self, days, is_buyer: bool) -> None:
        date_timestamp = (datetime.today() - timedelta(days=days)).timestamp()
        trades_cost = 0.0
        trades_quantity = 0.0
        for trade in self.my_trades:
            if trade["isBuyer"] == is_buyer and trade["time"] > date_timestamp:
                trades_cost += float(trade["quoteQty"])
                trades_quantity += float(trade["qty"])
        print(
            f"Trades for last {days} {'day' if days == 1 else 'days'}: "
            f"Average cost: {trades_cost / trades_quantity}"
        )
