import json
import requests
import config

def request_shared(pubkey):
    r = requests.get('%s/createshared/%s' % (config.API_ENDPOINT, pubkey))
    return r.json()


def request_signed(txid, vout, scriptPubKey, redeemScript):
    r = requests.get('%s/createsigned/%s-%d-%s-%s' % (
        config.API_ENDPOINT, txid, vout, scriptPubKey, redeemScript))
    return r.json()


def request_pubkey():
    r = requests.get('%s/getpubkey' % (config.API_ENDPOINT_WEB))
    return r.json()


def request_sign(rawTx, prevTxs, sigHashType, signingKey):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'rawtx': rawTx,
        'prevtxs': prevTxs,
        'sighashtype': sigHashType,
        'key': signingKey
    }
    url = '%s/sign' % (config.API_ENDPOINT_WEB)
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()
