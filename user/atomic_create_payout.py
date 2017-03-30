#!/usr/bin/env python
import sys

import server
from util import printJson


def AddPayout(rawTx, destination, amount):
    """
    Adds a payout output to the stub transaction.
    """
    result = server.omni_createrawtx_reference(rawTx, destination, amount)
    return result


def SealPayout(rawTx, txid, vout, scriptPubKey, redeemScript):
    """
    Seals and signs the stub transaction with payout.

    The transaction information must refer to the transaction input.
    """
    prevTxs = [{'txid': txid, 'vout': vout, 'scriptPubKey': scriptPubKey, 'redeemScript': redeemScript}]
    sigHashType = 'SINGLE|ANYONECANPAY'
    result = server.signrawtransaction(rawTx, prevTxs, None, sigHashType)
    return result


def help():
    print('atomic_create_payout rawtx destination amount\n')
    print('Adds a payout output and seals the input script.\n')
    print('Arguments:')
    print('1. rawtx         (string, required) the raw transaction to modify and sign')
    print('2. destination   (string, required) the payout destination')
    print('3. amount        (string, required) the payout amount\n')
    print('Example:')
    print('./atomic_create_payout.py \"01000000017cc61a1f458c039d57d8b3c5a1b97397d568c70bd0471b34d5b88768bf26b3e6000000'
          '009200483045022100930cb2947444a45e8fc2192d5d786bfb149facabc4b2c961c89faf69b06837ce0220033e62d8b8c32629dfed78'
          '870ac1125529a988856c9a1c53e78725e4995674b28247522103df84089a37a4794006a95d3acba0164d6f1f093ed073c986a017e1dc'
          '1a5a3d4f2103f5644417eefacb215f22f1faf525cb0ad93d73de560b91a3c496edbe3ee907d152aeffffffff0000000000\" '
          '\"mok6ijFnEyfcDDddK8ED6bxLYhfMupxepm\" \"0.25\"')
    exit()


def main():
    if len(sys.argv) > 1 and 'help' in str(sys.argv[1]):
        help()
    if len(sys.argv) != 4:
        help()

    rawTx = str(sys.argv[1])
    destination = str(sys.argv[2])
    amount = str(sys.argv[3])

    print("\nRequest:")
    print("  rawTx:       " + rawTx)
    print("  destination: " + destination)
    print("  amount:      " + amount)
    print("\nResponse:")

    result = AddPayout(rawTx, destination, amount)
    result = SealPayout(result)
    printJson(result)


if __name__ == "__main__":
    main()
