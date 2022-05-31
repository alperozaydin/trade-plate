import os


class LiqudityProvider:
    """
    For asset ids, check coingecko docs
    """

    LIQUDITY = [
        [
            "",  # pool id of LP
            ("nearpad", 0.10),  # first asset with purchase price in usd
            ("near", 6.00),  # second asset with purchase price in usd
            200,  # total cost in usd (combined)
        ]
    ]


class _WALLETS:
    _EVM_WALLET = None
    _NEAR_WALLET = None

    @property
    def EVM_WALLET(self):
        if not self._EVM_WALLET:
            self._EVM_WALLET = os.getenv("MY_EVM_WALLET_ADDRESS")
        return self._EVM_WALLET

    @property
    def NEAR_WALLET(self):
        if not self._NEAR_WALLET:
            self._NEAR_WALLET = os.getenv("MY_NEAR_WALLET_ADDRESS")
        return self._NEAR_WALLET


WALLETS: _WALLETS = _WALLETS()


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
        "near_panda_squad.near",
        "extinctheroes.tenk.near",
        "starry-night-by-markoethnear",
        "astropup.near",
        "undead.secretskelliessociety.near",
        "cartelgen1.neartopia.near",
    ]
