import random
from decimal import Decimal
from api import *
from server import *

def getpubkey(pubkeyhash=None):
    if pubkeyhash is None:
        pubkeyhash = getnewaddress()
    result = validateaddress(pubkeyhash)
    return result['pubkey']#, pubkeyhash

def getunspent(min_amount=0.0005):
    unspent = listunspent()
    random.shuffle(unspent)
    for output in unspent:
        if output['amount'] >= min_amount:
            return output
    raise Exception('No unspent output available')

def createpayback(rawtx, value):
    # add output
    return rawtx

def signpayback(rawtx):
    signrawtransaction
    # sign with SINGLE|ANYONECANPAY
    return rawtx

def createpayment(destination, fee=0.0001):
    unspent = getunspent()
    rawtx = createrawtransaction(
        [{
            'txid': unspent['txid'],
            'vout': unspent['vout']
        }],
        {
            destination['address']: 0.001 # TODO: insert amount!
        }
    )
    try:
        signed = signrawtransaction(
            rawtx=rawtx,
            vins=[{
                'txid': unspent['txid'],
                'vout': unspent['vout'],
                'scriptPubKey': unspent['scriptPubKey']
            }],
            sighashtype='ALL'
        )
    except JSONRPCException, e:
        raise Exception(e['error'])
    if signed['complete'] != True:
        raise Exception('Failed to sign transaction: %s' % (str(signed)))
    decoded = decoderawtransaction(signed['hex'])
    decoded['hex'] = signed['hex']
    decoded['source'] = unspent['address']
    return decoded

def test_shared():
    pubkey = getpubkey()
    destination = request_shared(pubkey)
    tx_funding = createpayment(destination)
    # only needed, if private key is not passed
    addmultisigaddress(len(destination['pubkeys']), destination['pubkeys'])
    request = {
        'txid': tx_funding['txid'],
        'vout': tx_funding['vout'][0]['n'],
        'scriptPubKey': tx_funding['vout'][0]['scriptPubKey']['hex'],
        'redeemScript': destination['redeemScript']
    }
    response = request_signed(
        request['txid'],
        request['vout'],
        request['scriptPubKey'],
        request['redeemScript']
    )
    signed_shared = signrawtransaction(
        rawtx=response['hex'],
        vins=[{
            'txid': request['txid'],
            'vout': request['vout'],
            'scriptPubKey': request['scriptPubKey'],
            'redeemScript': request['redeemScript']
        }],
        sighashtype='ALL'
    )
    return {
        'pubkey': pubkey,
        'destination': destination,
        'funding': tx_funding,
        'request': request,
        'unsigned': response,
        'signed': signed_shared
    }
