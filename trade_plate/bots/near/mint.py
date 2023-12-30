import asyncio
import json
import os

from py_near.account import Account
from pyonear.account_id import AccountId
from pyonear.crypto import InMemorySigner, KeyType

from trade_plate import Constants


class Mint:
    def __init__(
        self,
        account_id: str,
        private_key: str,
    ):
        self.account_id = account_id if account_id else os.getenv("NEAR_ACCOUNT_ID")
        self.private_key = (
            private_key if private_key else os.getenv("NEAR_ACCOUNT_PRIVATE_KEY")
        )
        self._private_keys = [self.private_key]
        self._account = None

    @property
    def account(self):
        if not self._account:
            self._account = Account(self.account_id, self.private_keys)
        return self._account

    @property
    def private_keys(self):
        if len(self._private_keys) == 1:
            keys_path = Constants.NEAR_KEYS_PATH

            with keys_path.open("r") as file:
                account_keys = json.load(file)
            try:
                self._private_keys.extend(account_keys[self.account_id])
            except KeyError as e:
                print(
                    f"{e}: No multi-keys found for {self.account_id}. "
                    f"Create some keys for multi-execution."
                )
        return self._private_keys

    async def create_private_keys(self, amount: int):
        for i in range(amount):
            signer = InMemorySigner.from_random(
                AccountId(self.account_id), KeyType.ED25519
            )
            await self.account.add_full_access_public_key(str(signer.public_key))
            self.private_keys.append(str(signer.secret_key))
        self._save_keys()
        print("NEAR KEYS SAVED.")

    async def call_contract(self, contract: str, method_name: str, method_arg: str):
        result = await self.account.function_call(
            contract_id=contract,
            method_name=method_name,
            args=json.loads(method_arg),
        )
        print("Task Result:", result.transaction_outcome.status)

    async def call_contract_bot(self, contract: str, method_name: str, method_arg: str):
        index = 1
        while index:
            tasks = []
            for _ in range(len(self.private_keys)):
                task = asyncio.create_task(
                    self.account.function_call(
                        contract_id=contract,
                        method_name=method_name,
                        args=json.loads(method_arg),
                    )
                )
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            for result in results:
                print("Task Result:", result.transaction_outcome.status)
            index += 1

    def _save_keys(self):
        keys_path = Constants.NEAR_KEYS_PATH
        near_path = keys_path.parent
        near_path.mkdir(parents=True, exist_ok=True)

        new_keys_data = {self.account_id: self.private_keys}

        if keys_path.is_file():
            with keys_path.open("r") as file:
                existing_keys_data = json.load(file)
        else:
            existing_keys_data = {}

        existing_keys_data.update(new_keys_data)

        with keys_path.open("w") as file:
            json.dump(existing_keys_data, file)
