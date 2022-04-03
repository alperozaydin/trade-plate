import click

from trade_plate.bots.nft_nint import near_nft_mint
from trade_plate.exchanges.binance.binance_plate import Binance
from trade_plate.constants import Constants
from trade_plate.tools.constants import LiqudityProvider

from trade_plate.utils import is_confirmed

from trade_plate.tools.iloss import Iloss


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
    for pool_id, asset_price_1, asset_price_2, cost in LiqudityProvider.LIQUDITY:
        il = Iloss(
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
    required=True,
)
@click.option(
    "--account_id",
    type=str,
    help="Account id which will execute the contract e.g. myaccount.near",
    default=None,
    requrired=True,
)
def nft_mint(
    nft_contract: str, mint_method_name: str, mint_method_arg: str, account_id: str
):
    near_nft_mint(
        nft_contract=nft_contract,
        mint_method_name=mint_method_name,
        mint_method_arg=mint_method_arg,
        account_id=account_id,
    )
