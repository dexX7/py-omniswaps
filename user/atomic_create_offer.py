#!/usr/bin/env python
import sys

from atomic_create_destination import CreateDestination
from atomic_create_payout import AddPayout, SealPayout
from atomic_prepare_funding import PrepareFunding
from atomic_publish_order import PublishOrder
from atomic_sign import GetSignedStub
import server
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
    value = fundingTx['output']['value']
    signingKey = destination['identifier']

    signedStubTx = GetSignedStub(txid, vout, scriptPubKey, redeemScript, signingKey)
    print('\nStub transaction:')
    printJson(signedStubTx)

    payoutStubTx = AddPayout(signedStubTx['hex'], fromAddress, amountDesired)
    print('\nPayout stub transaction:')
    printJson(payoutStubTx)

    signedPayoutStubTx = SealPayout(payoutStubTx, txid, vout, scriptPubKey, redeemScript)
    print('\nSigned payout stub:')
    printJson(signedPayoutStubTx)

    broadcastedTxid = server.sendrawtransaction(fundingTx['hex'])
    print('\nBroadcasted funding transaction:')
    print(broadcastedTxid)

    orderId = PublishOrder(signedPayoutStubTx['hex'], txid, vout, scriptPubKey, redeemScript, value)
    print('\nPublished offer:')
    printJson(orderId)

    return orderId


def help():
    print('atomic_create_offer address tokenid forsale desired\n')
    print('Prepares a signed transaction for an atomic swap.\n')
    print('Arguments:')
    print('1. address   (string, optional) the source for the tokens')
    print('3. tokenid   (string, optional) the identifier of the tokens to swap')
    print('3. forsale   (string, optional) the amount of tokens to swap')
    print('4. desired   (string, optional) the amount of coins desired in exchange\n')
    print('Example:')
    print('./atomic_create_offer.py \"mhtjwKYNZcvLbrvtvNVb4hTYDbfKgoCTx9\" 2 \"10.0\" \"1.0\"')
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

    CreateSwapOffer(fromAddress, tokenId, amountForSale, amountDesired)


if __name__ == "__main__":
    main()
