#!/usr/bin/env python
import sys

from api import requestAddOrder
from util import printJson


def PublishOrder(rawTx, txid, vout, scriptPubKey, redeemScript):
    """
    Publishes a swap-offer.
    """
    prevTxs = [{'txid': txid, 'vout': vout, 'scriptPubKey': scriptPubKey, 'redeemScript': redeemScript}]
    return requestAddOrder(rawTx, prevTxs)


def help():
    print('atomic_publish_order rawtx txid vout scriptPubKey redeemScript\n')
    print('Publishes a swap-offer.\n')
    print('Arguments:')
    print('1. rawtx          (string, required) the sealed offer as hex-encoded raw transaction\n')
    print('2. txid           (string, required) the hash of the funding transaction')
    print('3. vout           (number, required) the index of the funding output')
    print('4. scriptPubKey   (string, required) the scriptPubKey')
    print('5. redeemScript   (string, required) the redeemScript')
    print('Example:')
    print('./atomic_publish_order.py "0100000001cf03f6f5b775421ce8e0ff48ea0c17c0480e671d6e97500f8af25d8b02c008fa0200000'
          '0d90047304402206733c8eb0aaf02d7635e8a94202f01c284e993e7a13d19c861e44c4f99030e23022055f1951895f49b07468a95962'
          '4784146ef01a7f2e5f61a7176e186400f295ab08347304402207a2090e8e01a40c56271f35ab283216f33065c948e2162f254da376c3'
          '9d4c2f90220665de067ee3994c924618242c01e5ab571284e305190c85e93ac25c6029d9fb6824752210376b6bec94fe65e0cb43f713'
          '59a7c9287bf41066edb68f3a86e9c68d0190d19be2103dbc72f259e86fad518ed5c4b629977d8803f0e9696d4daf212be59cdbcc8b1d'
          '552aeffffffff0100e1f505000000001976a9141a0f165479f3a3c8f27e1c783739c553cd6f4f9788ac00000000" "fa08c0028b5df2'
          '8a0f50976e1d670e48c0170cea48ffe0e81c4275b7f5f603cf" 2 "a914efdeebbd7dd5f4723ddb34ebd33d61c102e8ba4b87" "5221'
          '0376b6bec94fe65e0cb43f71359a7c9287bf41066edb68f3a86e9c68d0190d19be2103dbc72f259e86fad518ed5c4b629977d8803f0e'
          '9696d4daf212be59cdbcc8b1d552ae"')
    exit()


def main():
    if len(sys.argv) > 1 and 'help' in str(sys.argv[1]):
        help()
    if len(sys.argv) != 6:
        help()

    rawTx = str(sys.argv[1])
    txid = str(sys.argv[2])
    vout = int(sys.argv[3])
    scriptPubKey = str(sys.argv[4])
    redeemScript = str(sys.argv[5])

    print('\nRequest:')
    print('  rawTx:        ' + rawTx)
    print('  txid:         ' + txid)
    print('  vout:         ' + str(vout))
    print('  scriptPubKey: ' + scriptPubKey)
    print('  redeemScript: ' + redeemScript)
    print('\nResponse:')

    result = PublishOrder(rawTx, txid, vout, scriptPubKey, redeemScript)
    printJson(result)


if __name__ == "__main__":
    main()
