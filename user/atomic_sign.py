#!/usr/bin/env python
import sys

import api as oracle
import server as rpc
from util import printJson


def GetSignedStub(txid, vout, scriptPubKey, redeemScript, signingKey):
    """
    Requests a script lock for the given output from the server.
    """
    prevTxs = [{'txid': txid, 'vout': vout, 'scriptPubKey': scriptPubKey, 'redeemScript': redeemScript}]
    txOuts = {}
    rawTxStub = rpc.createrawtransaction(prevTxs, txOuts)
    sigHashType = 'NONE|ANYONECANPAY'

    return oracle.requestSign(rawTxStub, prevTxs, sigHashType, signingKey)


def help():
    print('atomic_sign txid vout scriptPubKey redeemScript identifier\n')
    print('Lets the server sign a dummy transaction with, which can then be modified and extended.')
    print('Arguments:')
    print('1. txid           (string, required) the hash of the funding transaction')
    print('2. vout           (number, required) the index of the funding output')
    print('3. scriptPubKey   (string, required) the scriptPubKey')
    print('4. redeemScript   (string, required) the redeemScript')
    print('5. identifier     (string, required) the public key of the server, which was used to create the lock\n')
    print('Example:')
    print('./atomic_sign.py "e6b326bf6887b8d5341b47d00bc768d59773b9a1c5b3d8579d038c451f1ac67c" 0 "a9142e62eb4d8c1a85a18'
          '951d0819d8ff983e41be8f387" "522103df84089a37a4794006a95d3acba0164d6f1f093ed073c986a017e1dc1a5a3d4f2103f56444'
          '17eefacb215f22f1faf525cb0ad93d73de560b91a3c496edbe3ee907d152ae" "03f5644417eefacb215f22f1faf525cb0ad93d73de5'
          '60b91a3c496edbe3ee907d1"')
    exit()


def main():
    if len(sys.argv) > 1 and 'help' in str(sys.argv[1]):
        help()
    if len(sys.argv) != 6:
        help()

    txid = str(sys.argv[1])
    vout = int(sys.argv[2])
    scriptPubKey = str(sys.argv[3])
    redeemScript = str(sys.argv[4])
    signingKey = str(sys.argv[5])

    print("\nRequest:")
    print("  txid:         " + txid)
    print("  vout:         " + str(vout))
    print("  scriptPubKey: " + scriptPubKey)
    print("  redeemScript: " + redeemScript)
    print("  identifier:   " + signingKey)
    print("\nResponse:")

    result = GetSignedStub(txid, vout, scriptPubKey, redeemScript, signingKey)
    printJson(result)


if __name__ == "__main__":
    main()
