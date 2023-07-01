import os
from pathlib import Path


class LiqudityProvider:
    """
    For asset ids, check coingecko docs
    """

    LIQUDITY = [
        [
            "pze_visor",  # protocol id i.e aurora_nearpad
            "0x04c6b11E1Ffe1F1032BD62adb343C9D07767489c:5",  # pool id of LP
            (
                "ethereum",
                0.277526800746134339,
            ),  # first asset with purchase price in usd
            ("usd-coin", 998.881692),  # second asset with purchase price in usd
            1531.56,  # total cost in usd (combined)
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

    ACCESS_KEY = os.getenv("DEBANK_ACCESS_KEY")


class PROTOCOLS:
    AURORA_NEARPAD = "aurora_nearpad"


class PARAS:
    _BASE_URL = "https://api-v2-mainnet.paras.id"
    COLLECTION_STATS = f"{_BASE_URL}/collection-stats"
    COLLECTION_TOKEN = f"{_BASE_URL}/token"
    COLLECTION_OFFERS = f"{_BASE_URL}/offers"
    COLLECTIONS = f"{_BASE_URL}/collections"
    COLLECTION_ATTRIBUTES = f"{_BASE_URL}/collection-attributes"

    NFT_COLLECTIONS = [
        "mrbrownproject.near",
        "mara-smartcontract.near",
        "nft.pixacottaarmy.near",
        "near_panda_squad.near",
        "extinctheroes.tenk.near",
        "starry-night-by-markoethnear",
        "undead.secretskelliessociety.near",
        "cartelgen1.neartopia.near",
        "nearnautnft.near",
        "asac.near",
        "nearton_nft.near",
    ]


class PORTFOLIO:
    PATH = Path.home() / "local/crypto-pro-main.csv"
