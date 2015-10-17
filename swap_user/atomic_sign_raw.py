#!/usr/bin/env python
import sys

import simplejson

from api import requestSign
from util import printJson


def Sign(rawTx, prevTxs, sigHashType, signingKey):
    return requestSign(rawTx, prevTxs, sigHashType, signingKey)


def help():
    print("atomic_sign identifier rawtx prevtxs sighashtype\n")
    print("...\n")
    print("Arguments:")
    print("1. identifier    (string, required) the server's public key, which was used for the lock")
    print("2. rawtx         (string, required) the hex-encoded raw transaction to sign")
    print("3. prevtxs       (string, required) the previous transaction outputs")
    print("4. sighashtype   (string, required) the sighash type\n")
    print("Examples:")
    print("./atomic_sign.py \"02...55\" \"01000000000000000000\" \"[]\" \"NONE|ANYONECANPAY\"")
    exit()


def main():
    if len(sys.argv) > 1 and 'help' in str(sys.argv[1]):
        help()
    if len(sys.argv) != 5:
        help()

    signingKey = str(sys.argv[1])
    if signingKey == 'generate':
        from atomic_create_destination import CreatePubKey
        from atomic_create_destination import CreateDestination
        signingKey = CreateDestination(CreatePubKey())['identifier']
    rawTx = str(sys.argv[2])
    prevTxs = simplejson.loads(str(sys.argv[3]))
    sigHashType = str(sys.argv[4])

    print("\nRequest:")
    print("  identifier:  "+signingKey)
    print("  rawTx:       "+rawTx)
    print("  prevTxs:     "+str(prevTxs))
    print("  sigHashType: "+sigHashType)
    print("\nResponse:")

    result = Sign(rawTx, prevTxs, sigHashType, signingKey)
    printJson(result)


if __name__ == "__main__":
    main()
