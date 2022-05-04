import os


class LiqudityProvider:
    """
    For asset ids, check coingecko docs
    """

    LIQUDITY = [
        [
            "0x2aef68f92cfbafa4b542f60044c7596e65612d20",  # pool id of LP
            ("nearpad", 0.402),  # first asset with purchase price in usd
            ("near", 9.039),  # second asset with purchase price in usd
            2023.5,  # total cost in usd (combined)
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
    ]