import json
import uuid

import pytest
import requests

from trade_plate.tools.constants import LiqudityProvider, DeBankAPI, WALLETS
from trade_plate.tools.iloss import Iloss


@pytest.fixture
def mock_get_price(mocker):
    mocker.patch("trade_plate.tools.iloss.Iloss._get_current_price", return_value=0.1)


@pytest.fixture(scope="session")
def portfolio_data():
    with requests.session().get(
        DeBankAPI.PROTOCOL_URL,
        headers={"accept": "application/json", "AccessKey": DeBankAPI.ACCESS_KEY},
        params={"protocol_id": "pze_visor", "id": WALLETS.EVM_WALLET},
    ) as r:
        yield json.loads(r.content)


@pytest.mark.parametrize(
    "protocol_id, pool_id, asset_price_1, asset_price_2, cost",
    [
        ("id1", uuid.uuid4().hex, ("bitcoin", 5000), ("ethereum", 3000), 1000),
    ],
)
@pytest.mark.usefixtures("mock_get_price")
def test_iloss(protocol_id, pool_id, asset_price_1, asset_price_2, cost):
    asset1, _ = asset_price_1
    asset2, _ = asset_price_2
    il = Iloss(
        protocol_id=protocol_id,
        pool_id=pool_id,
        asset_price_1=asset_price_1,
        asset_price_2=asset_price_2,
        cost=cost,
    )
    price_ratio = il._price_ratio()
    iloss_value = il._iloss(price_ratio=price_ratio)

    assert round(iloss_value, 5) == -0.03175


@pytest.mark.skip(reason="No more free version of Debank")
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
