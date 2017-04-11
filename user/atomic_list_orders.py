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
    ordersWithFundingTxs = {}

    # add funding tx information from local node
    for key, value in list(ordersRaw.items()):
        tx = rpc.decoderawtransaction(value['rawtx'])
        fundingTxid = tx['vin'][0]['txid']
        value['fundingtx'] = rpc.omni_gettransaction(fundingTxid)
        ordersWithFundingTxs[key] = value

    return ordersWithFundingTxs


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
