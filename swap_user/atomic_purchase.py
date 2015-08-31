#!/usr/bin/env
import sys
import decimal
import random
import simplejson

import builder
from server import *


def print_json(parsed):
    print(simplejson.dumps(parsed, indent=2))


def extract_payload_script(rawtx):
    tx = decoderawtransaction(rawtx)
    for vout in tx['vout']:
        if vout ['scriptPubKey']['type'] == 'nulldata':
            script = vout['scriptPubKey']['hex']  # TODO: better detection
            return script
    raise Exception('No payload found!')


def extract_payment_value(rawtx):
    tx = decoderawtransaction(rawtx)
    return tx['vout'][0]['value']  # TODO: better extraction


def get_min_value_in(rawtx):
    value_fees = decimal.Decimal('0.0001')
    value_payment = extract_payment_value(rawtx)
    value_out = (2 * value_fees) + value_payment
    return value_out


def select_coins(min_value):
    selected_coins = []
    total = decimal.Decimal('0.00000000')
    unspent = listunspent()
    random.shuffle(unspent)
    for out in unspent:
        total += out['amount']
        selected_coins.append({'txid': out['txid'], 'vout': out['vout']})
        if (total >= min_value):
            break

    if (total < min_value):
        raise Exception('not enough coins')

    return selected_coins, total


def add_payload(rawtx, payload):
    size = payload[2:4]
    data = payload[4:]
    script = 'OP_RETURN 0x%s 0x%s' % (size, data)  # TODO: better construction
    rawtx = builder.outscript(rawtx, 0, script)
    return rawtx


def add_payment(rawtx, inputs):
    for vin in inputs:
        rawtx = builder.addin(rawtx, vin['txid'], vin['vout'])
    return rawtx


def add_reference(rawtx, destination, value_in):
    value_fees = decimal.Decimal('0.0001')
    value_payment = extract_payment_value(rawtx)
    value_out = value_fees + value_payment
    if (value_in < value_out):
        raise Exception('in  < out [%s < %s]' % (value_in, value_out))

    value_change = value_in - value_out
    if value_change < value_fees:
        raise Exception('change < fees')

    rawtx = builder.outaddr(rawtx, value_change, destination)
    return rawtx


def prepare_unsigned_payment(funding, rawtx, destination):
    payload = extract_payload_script(funding)
    value_needed = get_min_value_in(rawtx)
    selected_coins, total = select_coins(value_needed)

    rawtx = add_payment(rawtx, selected_coins)
    rawtx = add_payload(rawtx, payload)
    rawtx = add_reference(rawtx, destination, total)

    return rawtx


def prepare_payment(funding, rawtx, destination):
    rawtx = prepare_unsigned_payment(funding, rawtx, destination)
    result = signrawtransaction(rawtx)
    assert(result['complete'] == True)

    rawtx = result['hex']
    decoded = decoderawtransaction(rawtx)
    decoded['hex'] = rawtx

    return decoded


def print_blob_detail(blob):
    print_json(blob)


def print_blob(blob):
    print_json(blob['hex'])


def help():
    print("atomic_purchase fundingtx paymenttx destination\n")
    print("Prepares a signed transaction for the payment of an atomic swap.")

    exit()


def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        help()

    funding = str(sys.argv[1])
    payment = str(sys.argv[2])
    destination = str(sys.argv[3])

    swap = prepare_payment(funding, payment, destination)

    if len(sys.argv) > 4:
        print_blob_detail(swap)
    else:
        print_blob(swap)


if __name__ == "__main__":
    main()
