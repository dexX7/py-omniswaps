import decimal

import config
from bitcoinrpc.authproxy import AuthServiceProxy


rpc_connection = AuthServiceProxy('http://%s:%s@%s:%d' % (config.RPC_USER,
                                                          config.RPC_PASSWORD, config.RPC_CONNECT, config.RPC_PORT))


def EncodeDecimal(o):
    if isinstance(o, decimal.Decimal):
        return round(o, 8)
    raise TypeError(repr(o) + " is not JSON serializable (my!)")


def getinfo():
    return rpc_connection.getinfo()


def getbestblockhash():
    return rpc_connection.getbestblockhash()


def validateaddress(pubkeyhash):
    return rpc_connection.validateaddress(pubkeyhash)


def getnewaddress():
    return rpc_connection.getnewaddress()


def createrawtransaction(vins=[], vout={}):
    import json
    vout = json.loads(json.dumps(vout, default=EncodeDecimal))
    return rpc_connection.createrawtransaction(vins, vout)


def signrawtransaction(rawtx, vins=None, privkeys=None, sighashtype=None):
    return rpc_connection.signrawtransaction(rawtx, vins, privkeys, sighashtype)


def decoderawtransaction(rawtx):
    return rpc_connection.decoderawtransaction(rawtx)


def dumpprivkey(pubkeyhash):
    return rpc_connection.dumpprivkey(pubkeyhash)


def decodescript(rawscript):
    return rpc_connection.decodescript(rawscript)


def createmultisig(sigsreq=0, pubkeys=[]):
    return rpc_connection.createmultisig(sigsreq, pubkeys)


def addmultisigaddress(sigsreq=0, pubkeys=[]):
    return rpc_connection.addmultisigaddress(sigsreq, pubkeys)


def listunspent(minconf=0, maxconf=999999, addresses=[]):
    return rpc_connection.listunspent(minconf, maxconf, addresses)


def generate():
    return rpc_connection.generate(1)


def gettxout(txid, n):
    return rpc_connection.gettxout(txid, n)


def sendrawtransaction(rawtx, high_fees=True):
    return rpc_connection.sendrawtransaction(rawtx, high_fees)


def omni_setautocommit(flag):
    return rpc_connection.omni_setautocommit(flag)


def omni_send(from_address, to_address, token_id, amount, reference='0.01', redeem=''):
    return rpc_connection.omni_send(
        from_address, to_address, token_id, amount, redeem, reference)


def omni_createrawtx_reference(rawTx, destination, amount):
    amount = decimal.Decimal(amount)
    return rpc_connection.omni_createrawtx_reference(rawTx, destination, amount)


def omni_createrawtx_input(rawTx, txid, n):
    return rpc_connection.omni_createrawtx_input(rawTx, txid, n)


def omni_createrawtx_change(rawTx, prevTxs, destination, fee=decimal.Decimal('0.0001000'), position=0):
    return rpc_connection.omni_createrawtx_change(rawTx, prevTxs, destination, fee, position)


def omni_createrawtx_opreturn(rawTx, payload):
    return rpc_connection.omni_createrawtx_opreturn(rawTx, payload)


def omni_gettransaction(txid):
    return rpc_connection.omni_gettransaction(txid)
