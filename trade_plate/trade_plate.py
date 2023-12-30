import logging
from datetime import datetime

import click
from tabulate import tabulate

from trade_plate.constants import Constants
from trade_plate.exchanges.binance.binance_plate import Binance
from trade_plate.tools.constants import LiqudityProvider
from trade_plate.tools.iloss import Iloss
from trade_plate.tools.nft_marketplace.paras import Paras
from trade_plate.utils import is_confirmed

logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger()


@click.command()
@click.option(
    "--asset",
    type=str,
    help="Asset symbol with parity e.g. BTCUSDT",
    default=None,
    required=True,
)
@click.option(
    "--greed",
    type=str,
    help="Greedy level is how eager you are to get this asset",
    default="5",
    required=True,
)
def binance_plate_buy(asset: str, greed: str):
    asset = asset.upper()
    binance = Binance(
        asset=asset,
        greed=greed,
    )
    binance.trade_summary()

    max_price, min_price = None, None
    cache = Constants.CACHE.get(asset)
    if cache:
        max_price = cache.get("max_price")
        min_price = cache.get("min_price")

    max_value = click.prompt("Enter the max price", type=float, default=max_price)
    min_value = click.prompt("Enter the min price", type=float, default=min_price)
    assert min_value < max_value
    budget = click.prompt("Enter your budget", type=float)

    binance.create_buy_order(
        max_price=max_value,
        min_price=min_value,
        budget=budget,
        make_it=False,
    )

    if is_confirmed():
        binance.create_buy_order(
            max_price=max_value,
            min_price=min_value,
            budget=budget,
            make_it=True,
        )
        print("Orders created and made")
    else:
        print("No order made")


@click.command()
@click.option(
    "--asset",
    type=str,
    help="Asset symbol with parity e.g. BTCUSDT",
    default=None,
    required=True,
)
@click.option(
    "--greed",
    type=str,
    help="Greedy level is how you eager to get that asset",
    default="5",
    required=True,
)
def binance_plate_sell(asset: str, greed: str):
    asset = asset.upper()
    binance = Binance(
        asset=asset,
        greed=greed,
    )

    quantity = click.prompt("Enter your quantity", type=float)

    binance.create_sell_order(
        quantity=quantity,
        make_it=False,
    )

    if is_confirmed():
        binance.create_sell_order(
            quantity=quantity,
            make_it=True,
        )
        print(f"\n{Constants.OKGREEN}All orders are created.{Constants.OKGREEN}")

    else:
        print("No order made")


@click.command()
def iloss():
    for (
        protocol_id,
        pool_id,
        asset_price_1,
        asset_price_2,
        cost,
    ) in LiqudityProvider.LIQUDITY:
        il = Iloss(
            protocol_id=protocol_id,
            pool_id=pool_id,
            asset_price_1=asset_price_1,
            asset_price_2=asset_price_2,
            cost=cost,
        )
        il.run()


@click.option(
    "--collection",
    type=str,
    help="Name of the collection e.g. mrbrownproject.near",
    required=True,
)
@click.command()
def get_offers_collection(collection: str):
    paras = Paras(collection_id=collection)
    all_offers = paras.get_offers_collection()

    headers = ["Token ID", "Price", "Offeror", "Offer Date"]
    offers_data = []

    for offers in all_offers:
        for offer in offers:
            price = offer.get("price")
            if price:
                offers_data.append(
                    [
                        offer.get("token_id"),
                        f"{round(float(price) / 1e24, 2)} N",
                        offer.get("buyer_id"),
                        datetime.utcfromtimestamp(
                            offer.get("issued_at") / 1000
                        ).strftime("%Y-%m-%d %H:%M:%S"),
                    ]
                )

    print(tabulate(offers_data, headers=headers, tablefmt="grid"))
