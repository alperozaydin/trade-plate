import subprocess
import time
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class NftMint:
    def __init__(
        self,
        nft_contract: str,
        mint_method_name: str,
        mint_method_arg: str,
        account_id: str,
        force: bool,
    ):
        self.nft_contract = nft_contract
        self.mint_method_name = mint_method_name
        self.mint_method_arg = mint_method_arg
        self.account_id = account_id
        self.force = force

    def nft_mint(self):
        output = subprocess.run(
            [
                "near",
                "call",
                f"{self.nft_contract}",
                f"{self.mint_method_name}",
                f"{self.mint_method_arg}",
                "--account_id",
                self.account_id,
            ]
        )
        print(output)

    def setup_bot(self, mint_time_str: str):
        mint_time = datetime.strptime(mint_time_str, DATE_FORMAT)
        try_until = mint_time + timedelta(seconds=10)
        if self.force:
            try_until = mint_time + timedelta(hours=1)
        print(f"Mint bot started! Will try until: {try_until.strftime(DATE_FORMAT)}")
        while True:
            if try_until > datetime.utcnow() >= mint_time - timedelta(seconds=1):
                self.nft_mint()
                print(f"Mint ran on {datetime.now()}")
            time.sleep(0.01)
