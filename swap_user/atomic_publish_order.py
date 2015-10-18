#!/usr/bin/env python
import sys

from api import requestAddOrder
from util import printJson


def PublishOrder(order):
    """
    Publishes a swap-offer.
    """
    return requestAddOrder(order)


def help():
    print('atomic_publish_order rawtx\n')
    print('Publishes a swap-offer.\n')
    print('Arguments:')
    print('1. rawtx   (string, required) the sealed offer as hex-encoded raw transaction')
    print('Example:')
    print('./atomic_publish_order.py "01000000011ea1fdf020ef03557f25407bc35c40b93632a56148a795f10ed9cf517eba2d560200000'
          '0d90047304402204665731bfca0a56e42df41bceec11106b4d40acd345c23f10a2b3f01a5d38da302202645347c3d6c04b3663658bea'
          'fe5f8bc427625be0ad14b97b3f0543c225e006383473044022019f1dca981bc879b8a00bda138132fa5815f7eb4d0072222497462797'
          '277fac702204c60a8352da2e58ae34c3bd61204a402f4883a20e4038ec0dcf335b43eb5b26582475221031719d70c5909e1b9d40fa53'
          '0300b37d5cc9c6283dca94e62cf7702307269bfc42103d1679f8039dde841f5140a6c7068d0cd252d007de9a9b3a136c219a784df316'
          '052aeffffffff0100e1f505000000001976a91401ad66f81d5f4ef6e61ba4c34818de3899bf2e6788ac00000000')
    exit()


def main():
    if len(sys.argv) > 1 and 'help' in str(sys.argv[1]):
        help()
    if len(sys.argv) != 2:
        help()

    order = str(sys.argv[1])

    print('\nRequest:')
    print('  order: ' + order)
    print('\nResponse:')

    result = PublishOrder(order)
    printJson(result)


if __name__ == "__main__":
    main()
