# trade_plate

Crypto Trading & Monitoring Tool

## Project Features

* Give buy/sell orders on Binance (supports partial buy/sell orders for the given price range)
* NFT portfolio monitoring (on NEAR blockchain)
* Impermanent loss monitoring for your portfolio
* NFT mint from smart contract (NEAR blockchain) - very early stage

## Getting Started

Have followings installed on your machine:

* virtualenv for python
* python 3.8

`$ make venv`

`$ source venv/bin/activate`

`$ make build`

`$ trade-plate --help`

```buildoutcfg
Usage: trade-plate [OPTIONS] COMMAND [ARGS]...

  Console script for trade_plate.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  buy
  get_offers
  iloss
  mint
  mint_bot
  my_nft
  sell
```

### NEAR smart contract interaction

To interact with a smart contract:

```
trade-plate mint --contract <name of the contract> --method_name <name of the method> --method_arg '{}' --acount_id <your near wallet address> --private_key <private key of the account>
```

You can set the following env variable and run the mint command without 
passing account_id and private_key parameters

```
NEAR_ACCOUNT_ID=testacount.near
NEAR_ACCOUNT_PRIVATE_KEY=ed25519:private_key
```

It is possible to run the command in bot mode (Continuously calling the 
mint command forever until manually quiting the app). To do that, you need to create
multiple private keys.

Create private keys with the following command:

```
trade-plate mint --acount_id <your near wallet address> --private_key <private key of the account> --amount <the amount of private key>
```

It will create private keys and save it under `~.trade_plate/near/keys.json`
Then, add `--bot` flag to mint command for parallel execution.



## Resources

Below are some handy resource links.

* [Project Documentation](http://trade-plate.readthedocs.io/)
* [Click](http://click.pocoo.org/5/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.


## Authors

* **Alper Ozaydin** - [github](https://github.com/alperozaydin) - [website](https://alperozaydin.com)

## LicenseCopyright (c) Alper Ozaydin

All rights reserved.
