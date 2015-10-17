#!/usr/bin/env
import sys
import decimal
import simplejson

import builder
from atomic_create_destination import CreatePubKey, CreateDestination
from server import *
from api import requestSigned


def print_json(parsed):
    print(simplejson.dumps(parsed, indent=2))


def request_destination(from_address):
    pubkey = CreatePubKey()

    return CreateDestination(pubkey)['destination']


def find_funding_out(destination, tx):
    for vout in tx['vout']:
        if 'scriptPubKey' not in vout:
            continue
        if 'addresses' not in vout['scriptPubKey']:
            continue
        if destination['address'] in vout['scriptPubKey']['addresses']:
            return vout['n']

    raise Exception('invalid vout')


def get_stub(destination, tx):
    vout = find_funding_out(destination, tx)
    print('\nFunding vout:')
    print(vout)
    stub = requestSigned(
        tx['txid'], vout,
        destination['scriptPubKey'],
        destination['redeemScript']
    )
    print('requestSigned:')
    print(stub)

    return stub


def sign_payout(rawtx, destination, funding):
    vout = find_funding_out(destination, funding)
    signed = signrawtransaction(
        rawtx=rawtx,
        vins=[{
            'txid': funding['txid'], 'vout': vout,
            'scriptPubKey': destination['scriptPubKey'],
            'redeemScript': destination['redeemScript']
        }],
        sighashtype='SINGLE|ANYONECANPAY'
    )

    return signed['hex']


def get_signed_payout(blob, to_address, amount):
    stub = blob['stub']
    funding = blob['funding']
    destination = blob['destination']

    rawtx = stub['hex']
    rawtx = builder.outaddr(rawtx, amount, to_address)
    rawtx = sign_payout(rawtx, destination, funding)

    decoded = decoderawtransaction(rawtx)
    decoded['hex'] = rawtx

    return decoded


def prepare_funding(from_address, to_destination, token_id, amount):
    omni_setautocommit(False)
    rawtx = omni_send(from_address, to_destination, token_id, amount)
    omni_setautocommit(True)

    decoded = decoderawtransaction(rawtx)
    decoded['hex'] = rawtx

    return decoded


def prepare_initial(from_address, token_id, amount):
    destination = request_destination(from_address)
    print('\nDestination:')
    print(destination)
    tx = prepare_funding(from_address, destination['address'], token_id, amount)
    print('\nTransaction:')
    print(tx)
    stub = get_stub(destination, tx)
    print('\nStub:')
    print(stub)

    exit()

    result = {'destination': destination, 'funding': tx, 'stub': stub}
    return result


def prepare_offer(from_address, token_id, amount, desired):
    blob = prepare_initial(from_address, token_id, amount)
    blob['payment'] = get_signed_payout(blob, from_address, desired)

    return blob


def print_blob_detail(blob):
    print_json(blob)


def print_blob(blob):
    blob = {
        'funding':blob['funding']['hex'],
        'payment':blob['payment']['hex']
    }
    print_json(blob)


def help():
    print("atomic_create_offer address tokenid forsale desired\n")
    print("Prepares a signed transaction for an atomic swap.\n")
    print("Example:")
    print("atomic_create_offer muPnbit6RgucdziK5RsRhUueuhpkEvLk4t 2 10.0 1.0")
    exit()


def main():
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        help()

    address = str(sys.argv[1])
    tokenid = long(sys.argv[2])
    amount = str(sys.argv[3])
    desired = decimal.Decimal(sys.argv[4])

    offer = prepare_offer(address, tokenid, amount, desired)

    if len(sys.argv) > 5:
        print_blob_detail(offer)
    else:
        print_blob(offer)


if __name__ == "__main__":
    main()
