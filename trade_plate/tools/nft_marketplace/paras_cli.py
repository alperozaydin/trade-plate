import threading
from dataclasses import dataclass

import click
from tabulate import tabulate

from trade_plate.tools.constants import PARAS
from trade_plate.tools.nft_marketplace.paras import Paras


@dataclass
class CollectionsWorth:
    net_worth: int
    net_worth_usd: int


def get_collection(collection_id, nft_data, collections_worth, lock):
    collection = Paras(collection_id=collection_id)
    if collection.holding_amount:
        collection_value_usd = round(
            collection.get_near_price() * collection.collection_value, 2
        )
        with lock:
            nft_data.append(
                [
                    collection.collection_id,
                    collection.holding_amount,
                    f"{round(collection.floor_price, 2)} N",
                    f"{collection.collection_value} N (${collection_value_usd})",
                ]
            )
            collections_worth.net_worth += collection.collection_value
            collections_worth.net_worth_usd += collection_value_usd


@click.command()
def my_nft():
    headers = ["Collection Name", "Holding #", "Floor Price", "Net Worth"]
    nft_data = []

    collections_worth = CollectionsWorth(net_worth=0, net_worth_usd=0)
    lock = threading.Lock()
    threads = []

    for collection_id in PARAS.NFT_COLLECTIONS:
        thread = threading.Thread(
            target=get_collection,
            args=(collection_id, nft_data, collections_worth, lock),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    nft_data.append(
        [
            "TOTAL",
            "",
            "",
            f"{round(collections_worth.net_worth, 2)} N "
            f"(${round(collections_worth.net_worth_usd, 2)})",
        ]
    )

    print(tabulate(nft_data, headers=headers, tablefmt="grid"))
