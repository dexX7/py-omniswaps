import config
from bitcoinrpc.authproxy import AuthServiceProxy

rpc_connection = AuthServiceProxy('http://%s:%s@%s:%d' % (config.RPC_USER,
                                                          config.RPC_PASSWORD, config.RPC_CONNECT, config.RPC_PORT))


def EncodeDecimal(o):
    import decimal
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


def sendrawtransaction(rawtx, high_fees=True):
    return rpc_connection.sendrawtransaction(rawtx, high_fees)


def omni_setautocommit(flag):
    return rpc_connection.omni_setautocommit(flag)


def omni_send(from_address, to_address, token_id, amount, reference='0.0', redeem=''):
    return rpc_connection.omni_send(
        from_address, to_address, token_id, amount, redeem, reference)
