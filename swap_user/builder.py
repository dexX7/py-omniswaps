import subprocess

BITCOIN_TX = 'C:\\Users\\dexy\\Downloads\\omnicore-0.0.9.99-dev-win64\\omnicore-0.0.9.99-dev\\bin\\bitcoin-tx.exe'
BASE_ARGS = '-regtest'


def call_tx(rawtx, cmd=None):
    if cmd is None:
        return subprocess.check_output([BITCOIN_TX, '-regtest', rawtx])
    return subprocess.check_output([BITCOIN_TX, '-regtest', rawtx, cmd]).strip()


def show(rawtx):
    result = call_tx(rawtx)
    return result


def delin(rawtx, n):
    result = call_tx(rawtx, 'delin=%d' % n)
    return result


def delout(rawtx, n):
    result = call_tx(rawtx, 'delout=%d' % n)
    return result


def addin(rawtx, txid, vout):
    result = call_tx(rawtx, 'in=%s:%d' % (txid, vout))
    return result


def outaddr(rawtx, value, address):
    result = call_tx(rawtx, 'outaddr=%s:%s' % (value, address))
    return result


def outscript(rawtx, value, script):
    result = call_tx(rawtx, 'outscript=%s:%s' % (value, script))
    return result
