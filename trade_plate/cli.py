"""Console script for trade_plate."""
import click

from trade_plate.tools.nft_marketplace.paras_cli import my_nft
from trade_plate.trade_plate import (
    binance_plate_buy,
    binance_plate_sell,
    iloss,
    nft_mint,
    nft_mint_bot,
    get_offers_collection,
)
from trade_plate.version import __version__


@click.group()
@click.version_option(__version__)
def cli():
    """Console script for trade_plate."""
    pass


cli.add_command(binance_plate_buy, name="buy")
cli.add_command(binance_plate_sell, name="sell")
cli.add_command(iloss, name="iloss")
cli.add_command(nft_mint, name="mint")
cli.add_command(nft_mint_bot, name="mint_bot")
cli.add_command(my_nft, name="my_nft")
cli.add_command(get_offers_collection, name="get_offers")
