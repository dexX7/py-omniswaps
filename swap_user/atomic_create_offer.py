#!/usr/bin/env python
import sys

from atomic_create_destination import CreateDestination
from atomic_create_payout import AddPayout
from atomic_prepare_funding import PrepareFunding
from atomic_sign import GetSignedStub
from util import printJson


def CreateSwapOffer(fromAddress, tokenId, amountForSale, amountDesired):
    destination = CreateDestination()
    print('\nDestination:')
    printJson(destination)

    destinationAddress = destination['destination']['address']

    fundingTx = PrepareFunding(fromAddress, destinationAddress, tokenId, amountForSale)
    print('\nFunding transaction:')
    printJson(fundingTx)

    txid = fundingTx['output']['txid']
    vout = fundingTx['output']['vout']
    scriptPubKey = fundingTx['output']['scriptPubKey']
    redeemScript = destination['destination']['redeemScript']
    signingKey = destination['identifier']

    signedStubTx = GetSignedStub(txid, vout, scriptPubKey, redeemScript, signingKey)
    print('\nStub transaction:')
    printJson(signedStubTx)

    payoutStubTx = AddPayout(signedStubTx['hex'], destinationAddress, amountDesired)
    print('\nPayout stub transaction:')
    printJson(payoutStubTx)

    return payoutStubTx


def help():
    print("atomic_create_offer address tokenid forsale desired\n")
    print("Prepares a signed transaction for an atomic swap.\n")
    print("Example:")
    print("atomic_create_offer muPnbit6RgucdziK5RsRhUueuhpkEvLk4t 2 10.0 1.0")
    exit()


def main():
    if len(sys.argv) > 1 and 'help' in str(sys.argv[1]):
        help()
    if len(sys.argv) != 5:
        help()

    fromAddress = str(sys.argv[1])
    tokenId = long(sys.argv[2])
    amountForSale = str(sys.argv[3])
    amountDesired = str(sys.argv[4])

    print("\nRequest:")
    print("  fromAddress:   " + fromAddress)
    print("  tokenId:       " + str(tokenId))
    print("  amountForSale: " + amountForSale)
    print("  amountDesired: " + amountDesired)
    print("\nResponse:")

    result = CreateSwapOffer(fromAddress, tokenId, amountForSale, amountDesired)
    # printJson(result)


if __name__ == "__main__":
    main()
