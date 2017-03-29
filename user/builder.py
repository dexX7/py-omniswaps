import subprocess
import config



def call_tx(rawtx, cmd=None):
    if cmd is None:
        return subprocess.check_output([config.BITCOIN_TX, config.BITCOIN_TX_ARGS, rawtx])
    return subprocess.check_output([config.BITCOIN_TX, config.BITCOIN_TX_ARGS, rawtx, cmd]).strip()


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
