from trade_plate.tools.nft_marketplace.paras import Paras


def test_paras_api():
    paras = Paras(collection_id="mrbrownproject.near")
    assert paras.collection_data.get("collection_id") == "mrbrownproject.near"


def test_total_cards(mock_collection_data):
    paras = Paras(collection_id="mock_collection")
    paras._collection_data = mock_collection_data

    assert paras.total_cards == 4188


def test_collection_data_initial_call(mocker, mock_collection_stats_response):
    paras = Paras(collection_id="mock_collection")

    mock_get = mocker.patch.object(paras.session, "get")
    mock_get.return_value.__enter__.return_value = mock_collection_stats_response

    data = paras.collection_data
    assert data
    assert data.get("collection_id")
    assert data.get("total_cards")
    assert data.get("floor_price")


def test_collection_data(mocker, mock_collection_data):
    paras = Paras(collection_id="mock_collection")
    paras._collection_data = mock_collection_data

    mock_get = mocker.patch.object(paras.session, "get")
    mock_get.return_value.__enter__.return_value = None

    data = paras.collection_data
    assert data
    assert data.get("collection_id")
    assert data.get("total_cards")
    assert data.get("floor_price")


def test_holding_amount(mocker):
    paras = Paras(collection_id="mock_collection")
    mocker.patch.object(
        paras,
        "_get_nft_data_by_owner",
        return_value=[{"_id": "mock_id1"}, {"_id": "mock_id2"}],
    )

    assert paras.holding_amount == 2
