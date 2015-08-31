import flask
from flask import Flask

from model import rpc_connection

try:
    import simplejson as json
except ImportError:
    import json

##
# web server
##
app = Flask(__name__)

##
# routes for key generation
##
@app.route("/bestblockhash")
def show_bestblockhash():
    try:
        return rpc_connection.getbestblockhash()
    except Exception, e:
        print(e)
        return "rpc error"

@app.route('/validateaddress/<pubkeyhash>')
def show_validateaddress(pubkeyhash):
    return flask.jsonify(rpc_connection.validateaddress(pubkeyhash))

@app.route('/pubkey/<pubkeyhash>')
def show_pubkey(pubkeyhash):
    result = rpc_connection.validateaddress(pubkeyhash)
    return result['pubkey']

@app.route("/newaddress")
def show_newaddress():
    pubkeyhash = rpc_connection.getnewaddress()
    return show_validateaddress(pubkeyhash)

@app.route("/newmultisig")
@app.route("/newmultisig/<other_pubkey>")
def show_newmultisig(other_pubkey=None):
    pubkeyhash = rpc_connection.getnewaddress()
    pubkey = show_pubkey(pubkeyhash)
    pubkeys = [pubkey]
    if other_pubkey is not None:
        pubkeys.append(other_pubkey)
    pubkeys = sorted(pubkeys)
    try:
        result = rpc_connection.createmultisig(len(pubkeys), pubkeys)
    except Exception as e:
        print(e)
        return "error"
    script_info = rpc_connection.decodescript(result['redeemScript'])
    script_info['address'] = script_info['p2sh']
    script_info['pubkeys'] = pubkeys
    script_info['redeemScript'] = result['redeemScript']
    del script_info['addresses']
    del script_info['asm']
    del script_info['p2sh']
    return flask.jsonify(script_info)

##
# routes for dummy transaction
##
@app.route("/newtx/<txid>-<int:vout>")
def show_newtx(txid, vout):
    vins = [{"txid": txid, "vout": vout}]
    vout = {}
    try:
        rawtx = rpc_connection.createrawtransaction(vins, vout)
        decoded = rpc_connection.decoderawtransaction(rawtx)
        decoded['hex'] = rawtx
        return flask.jsonify(decoded)
    except Exception as e:
        print(e)
        return "error"


if __name__ == "__main__":
    app.run(debug=True)
