#!/usr/bin/env python
import sys

import api as oracle
import server as rpc
from util import printJson


def ListOrders():
    """
    Requests published orders.
    """
    ordersRaw = oracle.requestGetOrders()
    ordersWithInfo = {}

    # add funding tx and swap tx information from local node
    for key, value in list(ordersRaw.items()):
        tx = rpc.decoderawtransaction(value['rawtx'])
        fundingTxid = tx['vin'][0]['txid']
        fundingTxOut = rpc.gettxout(fundingTxid, tx['vin'][0]['vout'])
        fundingTx = rpc.omni_gettransaction(fundingTxid)

        status = 'not available'
        if fundingTxOut is not None:
            if fundingTx['confirmations'] > 0:
                status = 'confirmed'
            elif fundingTx['confirmations'] == 0:
                status = 'unconfirmed'

        value['fundingtx'] = fundingTx
        value['swaptx'] = tx
        value['status'] = status
        ordersWithInfo[key] = value

    return ordersWithInfo


def help():
    print('atomic_list_orders\n')
    print('Lists currently published orders.\n')
    print('Arguments:')
    print('None\n')
    print('Example:')
    print('./atomic_list_orders.py')
    exit()


def main():
    if len(sys.argv) > 1 and 'help' in str(sys.argv[1]):
        help()
    if len(sys.argv) != 1:
        help()

    print("\nResponse:")

    result = ListOrders()
    printJson(result)


if __name__ == "__main__":
    main()
