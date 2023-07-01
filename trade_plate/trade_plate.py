import logging
from datetime import datetime

import asyncclick as click
from tabulate import tabulate

from trade_plate.bots.nft_nint import NftMint
from trade_plate.exchanges.binance.binance_plate import Binance
from trade_plate.constants import Constants
from trade_plate.tools.constants import LiqudityProvider, PARAS
from trade_plate.tools.nft_marketplace.paras import Paras

from trade_plate.utils import is_confirmed

from trade_plate.tools.iloss import Iloss

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
    "--greedy",
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


@click.command()
@click.option(
    "--nft_contract",
    type=str,
    help="Contract ID e.g. nft.thedons.near",
    default=None,
    required=True,
)
@click.option(
    "--mint_method_name",
    type=str,
    help="Name of the mint method e.g. nft_mint_one",
    default=None,
    required=True,
)
@click.option(
    "--mint_method_arg",
    type=str,
    help="Argument for the mint method if it is needed",
    default="{}",
    required=False,
    show_default=True,
)
@click.option(
    "--account_id",
    type=str,
    help="Account id which will execute the contract e.g. myaccount.near",
    default=None,
    required=True,
)
def nft_mint(
    nft_contract: str, mint_method_name: str, mint_method_arg: str, account_id: str
):
    NftMint(
        nft_contract=nft_contract,
        mint_method_name=mint_method_name,
        mint_method_arg=mint_method_arg,
        account_id=account_id,
    ).nft_mint()


@click.command()
@click.option(
    "--nft_contract",
    type=str,
    help="Contract ID e.g. nft.thedons.near",
    default=None,
    required=True,
)
@click.option(
    "--mint_method_name",
    type=str,
    help="Name of the mint method e.g. nft_mint_one",
    default=None,
    required=True,
)
@click.option(
    "--mint_method_arg",
    type=str,
    help="Argument for the mint method if it is needed",
    default="{}",
    required=False,
    show_default=True,
)
@click.option(
    "--account_id",
    type=str,
    help="Account id which will execute the contract e.g. myaccount.near",
    default=None,
    required=True,
)
@click.option(
    "--mint_time",
    type=str,
    help="Mint time in UTC timezone. Format: '2018-06-29 08:15:27.243860'",
    required=True,
)
@click.option(
    "--force",
    type=bool,
    help="Force to mint like there is no tomorrow LOL",
    is_flag=True,
    default=False,
    required=False,
)
def nft_mint_bot(
    nft_contract: str,
    mint_method_name: str,
    mint_method_arg: str,
    account_id: str,
    mint_time: str,
    force: bool,
):
    NftMint(
        nft_contract=nft_contract,
        mint_method_name=mint_method_name,
        mint_method_arg=mint_method_arg,
        account_id=account_id,
        force=force,
    ).setup_bot(mint_time_str=mint_time)


@click.command()
def my_nft():
    headers = ["Collection Name", "Holding #", "Floor Price", "Net Worth"]
    nft_data = []

    net_worth = 0
    net_worth_usd = 0
    for collection_id in PARAS.NFT_COLLECTIONS:
        collection = Paras(collection_id=collection_id)
        if collection.holding_amount:
            collection_value_usd = round(
                collection.get_near_price() * collection.collection_value, 2
            )
            nft_data.append(
                [
                    collection.collection_id,
                    collection.holding_amount,
                    f"{round(collection.floor_price, 2)} N",
                    f"{collection.collection_value} N (${collection_value_usd})",
                ]
            )
            net_worth += collection.collection_value
            net_worth_usd += collection_value_usd

    nft_data.append(
        ["TOTAL", "", "", f"{round(net_worth, 2)} N (${round(net_worth_usd, 2)})"]
    )

    print(tabulate(nft_data, headers=headers, tablefmt="grid"))


@click.option(
    "--collection",
    type=str,
    help="Name of the collection e.g. mrbrownproject.near",
    required=True,
)
@click.option(
    "--concurrent",
    type=bool,
    help="Run the command with async functionality",
    is_flag=True,
    default=False,
    required=True,
)
@click.command()
async def get_offers_collection(collection: str, concurrent: bool):
    paras = Paras(collection_id=collection)
    if concurrent:
        all_offers = paras.get_offers_collection_async()
    else:
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
