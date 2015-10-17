#!/usr/bin/env python
import sys

import server
from util import printJson


def findFundingOutput(destination, rawTx):
    tx = server.decoderawtransaction(rawTx)
    for vout in tx['vout']:
        if 'scriptPubKey' not in vout:
            continue
        if 'addresses' not in vout['scriptPubKey']:
            continue
        if destination not in vout['scriptPubKey']['addresses']:
            continue

        result = {
            'txid': tx['txid'],
            'vout': vout['n'],
            'scriptPubKey': vout['scriptPubKey']['hex']
        }
        return result

    raise Exception('invalid transaction')


def PrepareFunding(fromAddress, destination, tokenId, amount):
    server.omni_setautocommit(False)
    rawTx = server.omni_send(fromAddress, destination, tokenId, amount)
    server.omni_setautocommit(True)

    fundingOutput = findFundingOutput(destination, rawTx)
    result = {
        'hex': rawTx,
        'output': fundingOutput
    }

    return result


def help():
    print('atomic_prepare_funding ddress destination tokenid amount\n')
    print('Prepares a raw transaction to fund a script locked destination.\n')
    print('Arguments:')
    print('1. address       (string, optional) the source for the tokens')
    print('2. destination   (string, optional) the funding destination')
    print('3. tokenid       (string, optional) the identifier of the tokens to swap')
    print('4. amount        (string, optional) the amount of tokens to swap\n')
    print('Example:')
    print('./atomic_prepare_funding.py \"mffphSgNTrXAF2dZMQTdkVWXbjAJkWD4VU\" \"2NFBZPk3t767N9K3oSrM575sioZXq3V7TZU\" 2'
          ' \"0.1\"')
    exit()


def main():
    if len(sys.argv) > 1 and 'help' in str(sys.argv[1]):
        help()
    if len(sys.argv) != 5:
        help()

    fromAddress = str(sys.argv[1])
    destination = str(sys.argv[2])
    tokenId = long(sys.argv[3])
    amount = str(sys.argv[4])

    print("\nRequest:")
    print("  fromAddress: " + fromAddress)
    print("  destination: " + destination)
    print("  tokenId:     " + str(tokenId))
    print("  amount:      " + amount)
    print("\nResponse:")

    result = PrepareFunding(fromAddress, destination, tokenId, amount)
    printJson(result)


if __name__ == "__main__":
    main()
