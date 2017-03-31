#!/usr/bin/env python
import random
import sys
from decimal import Decimal

import api as oracle
import server as rpc
from atomic_unpublish_order import UnpublishOrder
from util import printJson


def ExtractValueIn(rawTx):
    return Decimal('0.00000000')  # TODO: better extraction


def ExtractValueOut(rawTx):
    tx = rpc.decoderawtransaction(rawTx)
    valueOut = Decimal('0.00000000')
    for out in tx['vout']:
        valueOut += out['value']
    return valueOut


def ExtractPaymentValue(rawTx, txFees=Decimal('0.00010000')):
    valueIn = ExtractValueIn(rawTx)
    valueOut = ExtractValueOut(rawTx) + txFees
    return valueIn - valueOut


def SelectCoins(valueNeeded):
    valueIn = Decimal('0.00000000')
    prevTxs = []

    unspentTxOuts = rpc.listunspent()
    random.shuffle(unspentTxOuts)
    for out in unspentTxOuts:
        valueIn += out['amount']
        prevTxs.append({
            'txid': out['txid'],
            'vout': out['vout'],
            'scriptPubKey': out['scriptPubKey'],
            'value': out['amount'],
        })
        if valueIn >= valueNeeded:
            break
    if valueIn < valueNeeded:
        raise Exception('ERROR: not enough coins')

    return prevTxs


def AcceptOrder(orderId, destination):
    """
    Accepts and pays for an order.
    """
    orders = oracle.requestGetOrders()
    if orderId not in orders:
        raise Exception('ERROR: order id %s not listed' % orderId)
    order = orders[orderId]
    rawTx = order['rawtx']
    prevTxs = order['prevtxs']
    valueNeeded = ExtractPaymentValue(rawTx)
    prevTxsToAdd = SelectCoins(valueNeeded)
    prevTxs = prevTxs + prevTxsToAdd

    print('\nPrevious outputs:')
    printJson(prevTxs)

    # add inputs
    for out in prevTxsToAdd:
        rawTx = rpc.omni_createrawtx_input(rawTx, out['txid'], out['vout'])

    # add payload
    payload = '0000000402'  # send-all test ecosystem # TODO: remove ecosystem magic
    rawTx = rpc.omni_createrawtx_opreturn(rawTx, payload)

    # make change and reference
    rawTx = rpc.omni_createrawtx_change(rawTx, prevTxs, destination, position=999999) # TODO: reference may be added

    # sign
    signedTx = rpc.signrawtransaction(rawTx, prevTxs)

    print('\nSigned transaction:')
    printJson(signedTx)

    # broadcast
    result = rpc.sendrawtransaction(signedTx['hex'])

    # remove order
    UnpublishOrder(orderId)

    return result


def help():
    print('atomic_accept_order orderid destination\n')
    print('Accepts and pays for an order.\n')
    print('Arguments:')
    print('1. orderid       (string, required) the identifier of the order')
    print('2. destination   (string, required) the destination for the tokens\n')
    print('Example:')
    print('./atomic_accept_order.py "54e2e8f5bd945c751d166dea4d6512b324ef5053cc28adaf0fbeca705f5a8ce3" '
          '"n2VV1Z6azGHJWdzLyXkFjQhHqbWjmM7cuh"')
    exit()


def main():
    if len(sys.argv) > 1 and 'help' in str(sys.argv[1]):
        help()
    if len(sys.argv) != 3:
        help()

    orderId = str(sys.argv[1])
    destination = str(sys.argv[2])

    print('\nRequest:')
    print('  orderId: ' + orderId)
    print('  destination: ' + destination)
    print('\nResponse:')

    result = AcceptOrder(orderId, destination)
    printJson(result)


if __name__ == "__main__":
    main()
