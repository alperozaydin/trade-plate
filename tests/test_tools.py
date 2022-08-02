import json

import pytest
import uuid

import requests

from trade_plate.tools.constants import LiqudityProvider, DeBankAPI, PROTOCOLS, WALLETS
from trade_plate.tools.iloss import Iloss
from trade_plate.tools.nft_marketplace.paras import Paras


@pytest.fixture
def mock_get_price(mocker):
    mocker.patch("trade_plate.tools.iloss.Iloss._get_current_price", return_value=0.1)


@pytest.fixture(scope="session")
def portfolio_data():
    with requests.session().get(
        DeBankAPI.PROTOCOL_URL,
        params={"protocol_id": PROTOCOLS.AURORA_NEARPAD, "id": WALLETS.EVM_WALLET},
    ) as r:
        yield json.loads(r.content)


@pytest.mark.parametrize(
    "pool_id, asset_price_1, asset_price_2, cost",
    [
        (uuid.uuid4().hex, ("bitcoin", 5000), ("ethereum", 3000), 1000),
    ],
)
@pytest.mark.usefixtures("mock_get_price")
def test_iloss(pool_id, asset_price_1, asset_price_2, cost):
    asset1, _ = asset_price_1
    asset2, _ = asset_price_2
    il = Iloss(
        pool_id=pool_id,
        asset_price_1=asset_price_1,
        asset_price_2=asset_price_2,
        cost=cost,
    )
    price_ratio = il._price_ratio()
    iloss_value = il._iloss(price_ratio=price_ratio)

    assert round(iloss_value, 5) == -0.03175


def test_paras_api():
    paras = Paras(collection_id="mrbrownproject.near")
    assert paras


@pytest.mark.skip(reason="Probably, the pool is deleted")
@pytest.mark.parametrize(
    "pool_id, pool_exists",
    [(LiqudityProvider.LIQUDITY[0][0], True), (uuid.uuid4().hex, False)],
)
def test_pad_fi_lp_pool_exists(portfolio_data, pool_exists, pool_id):
    for portfolio in portfolio_data.get("portfolio_item_list"):
        if portfolio.get("pool").get("id") == pool_id:
            assert pool_exists
            return

    assert not pool_exists
