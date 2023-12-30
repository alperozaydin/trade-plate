import json

from trade_plate.bots.near.mint import Mint

ACCOUNT_ID = "foo.bar"
PRIVATE_KEY = "ed25519:bar"


def test_save_keys(tmp_path, mocker):
    keys_path = tmp_path / "keys.json"
    mocker.patch("trade_plate.constants.Constants.NEAR_KEYS_PATH", keys_path)

    mint = Mint(
        account_id=ACCOUNT_ID,
        private_key=PRIVATE_KEY,
    )
    private_keys = ["ed25519:key1", "ed25519:key2"]
    mint._private_keys = private_keys
    mint._save_keys()

    # Save keys with another account and test both account information is available

    mint = Mint(
        account_id="test.account",
        private_key=PRIVATE_KEY,
    )
    private_keys_2 = ["ed25519:key3", "ed25519:key4"]
    mint._private_keys = private_keys_2

    mint._save_keys()

    with keys_path.open("r") as file:
        keys = json.load(file)

    assert len(keys.keys()) == 2
    assert keys[ACCOUNT_ID] == private_keys
    assert keys["test.account"] == private_keys_2
