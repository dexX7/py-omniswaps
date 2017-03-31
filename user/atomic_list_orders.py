#!/usr/bin/env python
import sys

import api as oracle
from util import printJson


def ListOrders():
    """
    Requests published orders.
    """
    return oracle.requestGetOrders()


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
