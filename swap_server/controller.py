from MemoryKeyRepository import MemoryKeyRepository
from server import *


class Controller:
    def __init__(self):
        rpcServer = AuthServiceProxy(
            'http://%s:%s@%s:%d' % (config.RPC_USER, config.RPC_PASSWORD, config.RPC_CONNECT, config.RPC_PORT))
        self.repository = MemoryKeyRepository(rpcServer)

    def GetNextPubKey(self):
        return self.repository.GetNextPubKey()

    def Sign(self, rawTx, vIns, sigHashType, signingKey):
        return self.repository.SignTransaction(rawTx, vIns, sigHashType, signingKey)


# DEPRECIATED
def getpubkey(pubkeyhash=None):
    if pubkeyhash is None:
        pubkeyhash = getnewaddress()
    result = validateaddress(pubkeyhash)
    return result['pubkey']


# DEPRECIATED
def getscriptpubkey(pubkeyhash):
    result = validateaddress(pubkeyhash)
    return result['scriptPubKey']


# DEPRECIATED
def createshared(other_pubkey):
    pubkey = getpubkey()
    pubkeys = sorted([pubkey, other_pubkey])
    response_create = createmultisig(len(pubkeys), pubkeys)
    response_script = decodescript(response_create['redeemScript'])
    addmultisigaddress(len(pubkeys), pubkeys)
    result = {
        'address': response_script['p2sh'],
        'pubkeys': pubkeys,
        'redeemScript': response_create['redeemScript'],
        'reqSigs': response_script['reqSigs'],
        'scriptPubKey': getscriptpubkey(response_script['p2sh']),
        'type': response_script['type'],
    }
    return result


# DEPRECIATED
def createunsigned(txid, vout):
    rawtx = createrawtransaction([{'txid': txid, 'vout': vout}])
    decoded = decoderawtransaction(rawtx)
    return {
        "hex": rawtx,
        'txid': decoded['txid'],
        'version': decoded['version'],
        'locktime': decoded['locktime'],
        'vin': decoded['vin'],
        'vout': decoded['vout'],
    }


# DEPRECIATED
# TOOD: must not sign any other than original! request + sign must be atomic!
def createsigned(txid, vout, scriptPubKey, redeemScript):
    rawtx = createunsigned(txid, vout)['hex']
    signresult = signrawtransaction(rawtx, [{
        'txid': txid,
        'vout': vout,
        'scriptPubKey': scriptPubKey,
        'redeemScript': redeemScript
    }], 'NONE|ANYONECANPAY')
    rawtx = signresult['hex']
    decoded = decoderawtransaction(rawtx)
    return {
        'hex': rawtx,
        'txid': decoded['txid'],
        'version': decoded['version'],
        'locktime': decoded['locktime'],
        'vin': decoded['vin'],
        'vout': decoded['vout'],
    }
