py-omniswaps
============

This repository contains code to generate atomic swaps for Omni Layer  tokens, with the help of an oracle.

The `server` directory contains a very rudimentary in-memory oracle, which is accessible via a REST API.

The `user` directory contains scripts for the user, who can create or accept orders with `atomic_create_offer.py` and
`atomic_accept_order.py`. Orders can be listed with `atomic_list_orders.py`. The configuration file `user/config.py`
needs to be updated accordingly. Each script has a help description, which is shown when running `./script.py help`.

Currently an oracle is running in testnet/regtest mode on `http://api.bitwatch.co:5000`. The state can be reset by
visiting `http://api.bitwatch.co:5000/reset`.

PLEASE BE AWARE THIS IS NOT COMPLETE AND JUST A PROOF OF CONCEPT. DO NOT USE WITH REAL FUNDS!
