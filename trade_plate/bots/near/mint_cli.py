import asyncio
import click

from trade_plate.bots.near.mint import Mint


@click.command()
@click.option(
    "--contract",
    type=str,
    help="Contract ID e.g. awesomenfts.near",
    default=None,
    required=True,
)
@click.option(
    "--method_name",
    type=str,
    help="Name of the method e.g. nft_mint_one",
    default=None,
    required=True,
)
@click.option(
    "--method_arg",
    type=str,
    help="Arguments for method if it is needed",
    default="{}",
    required=False,
    show_default=True,
)
@click.option(
    "--account_id",
    type=str,
    help="Account id which will execute the contract e.g. myaccount.near",
    default=None,
    required=False,
)
@click.option(
    "--private_key",
    type=str,
    help="Private key of the account e.g. ed25519;....",
    default=None,
    required=False,
)
@click.option(
    "--bot",
    type=bool,
    is_flag=True,
    help="Run the contract forever. You are a bot.",
    default=False,
    required=False,
)
def mint(
    contract: str,
    method_name: str,
    method_arg: str,
    account_id: str,
    private_key: str,
    bot: bool,
):
    mint_ = Mint(
        account_id=account_id,
        private_key=private_key,
    )
    if not bot:
        asyncio.run(
            mint_.call_contract(
                contract=contract, method_name=method_name, method_arg=method_arg
            )
        )
    else:
        asyncio.run(
            mint_.call_contract_bot(
                contract=contract, method_name=method_name, method_arg=method_arg
            )
        )


@click.option(
    "--amount",
    type=int,
    help="Amount of private keys to be created",
    default=10,
    required=False,
)
@click.option(
    "--account_id",
    type=str,
    help="Account id which will execute the contract e.g. myaccount.near",
    default=None,
    required=False,
)
@click.option(
    "--private_key",
    type=str,
    help="Private key of the account e.g. ed25519;....",
    default=None,
    required=False,
)
def create_keys(account_id: str, private_key: str, amount: int):
    mint = Mint(
        account_id=account_id,
        private_key=private_key,
    )
    mint.create_private_keys(amount=amount)
