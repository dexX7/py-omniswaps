import simplejson as json
import requests
import config


# Depreciated
def requestShared(pubkey):
    r = requests.get('%s/createshared/%s' % (config.API_ENDPOINT, pubkey))
    return r.json()


# Depreciated
def requestSigned(txid, vout, scriptPubKey, redeemScript):
    r = requests.get('%s/createsigned/%s-%d-%s-%s' % (
        config.API_ENDPOINT, txid, vout, scriptPubKey, redeemScript))
    return r.json()


def requestPubkey():
    r = requests.get('%s/getpubkey' % config.API_ENDPOINT_WEB)
    return r.json()


def requestSign(rawTx, prevTxs, sigHashType, signingKey):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'rawtx': rawTx,
        'prevtxs': prevTxs,
        'sighashtype': sigHashType,
        'key': signingKey
    }
    url = '%s/sign' % config.API_ENDPOINT_WEB
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()


def requestGetOrder(orderId):
    r = requests.get('%s/getorder/%s' % (config.API_ENDPOINT_WEB, orderId))
    return r.json()


def requestGetOrders():
    r = requests.get('%s/getorders' % config.API_ENDPOINT_WEB)
    return r.json()


def requestAddOrder(rawTx, prevTxs):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'rawtx': rawTx,
        'prevtxs': prevTxs
    }
    url = '%s/addorder' % config.API_ENDPOINT_WEB
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()


def requestRemoveOrder(orderId):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'identifier': orderId
    }
    url = '%s/removeorder' % config.API_ENDPOINT_WEB
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()
