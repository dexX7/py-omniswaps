import config
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_connection = AuthServiceProxy('http://%s:%s@%s:%d' % (config.RPC_USER,
    config.RPC_PASSWORD, config.RPC_CONNECT, config.RPC_PORT))

def getinfo():
    return rpc_connection.getinfo()

def getbestblockhash():
    return rpc_connection.getbestblockhash()

def validateaddress(pubkeyhash):
    return rpc_connection.validateaddress(pubkeyhash)

def getnewaddress():
    return rpc_connection.getnewaddress()

def createrawtransaction(vins=[], vout={}):
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

def listunspent():
    return rpc_connection.listunspent()

def generate():
    return rpc_connection.generate(1)

def sendrawtransaction(rawtx, high_fees=True):
    return rpc_connection.sendrawtransaction(rawtx, high_fees)
