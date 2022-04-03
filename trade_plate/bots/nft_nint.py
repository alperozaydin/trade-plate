import subprocess


def near_nft_mint(
    nft_contract: str, mint_method_name: str, mint_method_arg: str, account_id: str
):
    output = subprocess.run(
        [
            "near",
            "call",
            f"{nft_contract}",
            f"{mint_method_name}",
            f"{mint_method_arg}",
            "--account_id",
            account_id,
        ]
    )
    print(output)
    print(output.returncode)
