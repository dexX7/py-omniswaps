import requests
import simplejson as json

import config


def requestPubkey():
    r = requests.get('%s/getpubkey' % config.API_ENDPOINT)
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
    url = '%s/sign' % config.API_ENDPOINT
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()


def requestGetOrder(orderId):
    r = requests.get('%s/getorder/%s' % (config.API_ENDPOINT, orderId))
    return r.json()


def requestGetOrders():
    r = requests.get('%s/getorders' % config.API_ENDPOINT)
    return r.json()


def requestAddOrder(rawTx, prevTxs):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'rawtx': rawTx,
        'prevtxs': prevTxs
    }
    url = '%s/addorder' % config.API_ENDPOINT
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()


def requestRemoveOrder(orderId):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'identifier': orderId
    }
    url = '%s/removeorder' % config.API_ENDPOINT
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()
