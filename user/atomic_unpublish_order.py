#!/usr/bin/env python
import sys

from api import requestRemoveOrder
from util import printJson


def UnpublishOrder(orderId):
    """
    Unpublishes a swap-offer.
    """
    return requestRemoveOrder(orderId)


def help():
    print('atomic_unpublish_order orderid\n')
    print('Unpublishes an order.\n')
    print('Arguments:')
    print('1. orderid   (string, required) the identifier of the order\n')
    print('Example:')
    print('./atomic_unpublish_order.py "7ea91f941e7feb07ef854e57b55ee88bcda829055836ec472db6bc9b68e99338"')
    exit()


def main():
    if len(sys.argv) > 1 and 'help' in str(sys.argv[1]):
        help()
    if len(sys.argv) != 2:
        help()

    orderId = str(sys.argv[1])

    print('\nRequest:')
    print('  orderId: ' + orderId)
    print('\nResponse:')

    result = UnpublishOrder(orderId)
    printJson(result)


if __name__ == "__main__":
    main()
