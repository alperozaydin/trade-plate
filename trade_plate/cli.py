"""Console script for trade_plate."""
import click
from trade_plate.trade_plate import binance_plate_buy, binance_plate_sell
from trade_plate.version import __version__


@click.group()
@click.version_option(__version__)
def cli():
    """Console script for trade_plate."""
    pass


cli.add_command(binance_plate_buy, name="buy")
cli.add_command(binance_plate_sell, name="sell")
