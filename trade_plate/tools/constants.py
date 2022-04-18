class LiqudityProvider:
    """
    For asset ids, check coingecko docs
    """

    LIQUDITY = [
        [
            "pool_id",  # pool id of LP
            ("first_asset", 1),  # first asset with purchase price in usd
            ("second_asset", 1),  # second asset with purchase price in usd
            1000,  # total cost in usd (combined)
        ]
    ]


class WALLETS:
    EVM_WALLET = "my evm wallet address"  # MM wallet address
    NEAR_WALLET = "my near wallet address"


class DeBankAPI:
    _BASE_URL = "https://openapi.debank.com/"
    PROTOCOL_URL = f"{_BASE_URL}/v1/user/protocol"


class PROTOCOLS:
    AURORA_NEARPAD = "aurora_nearpad"


class PARAS:
    _BASE_URL = "https://api-v2-mainnet.paras.id"
    COLLECTION_STATS = f"{_BASE_URL}/collection-stats"
    COLLECTION_TOKEN = f"{_BASE_URL}/token"

    NFT_COLLECTIONS = [
        "mrbrownproject.near",
        "mara-smartcontract.near",
        "nft.pixacottaarmy.near",
        "nft.pixacottaarmy.near",
        "near_panda_squad.near",
        "extinctheroes.tenk.near",
        "thebullishbulls.near",
        "futurenft.near",
        "starry-night-by-markoethnear",
    ]
