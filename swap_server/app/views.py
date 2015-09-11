from flask import make_response, jsonify
from app import app
from controller import *

@app.errorhandler(404)
def not_found_error(error):
    return make_response(jsonify({'error': 'not found'}), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'error': 'internal server error'}), 500)

@app.route('/pubkey')
@app.route('/pubkey/<pubkeyhash>')
def pubkey(pubkeyhash=None):
    return jsonify({'pubkey': getpubkey(pubkeyhash)})

@app.route('/createshared/<pubkey>')
def destination(pubkey):
    return jsonify(createshared(pubkey))

@app.route('/createunsigned/<txid>-<int:vout>')
def unsigned(txid, vout):
    return jsonify(createunsigned(txid, vout))

@app.route('/createsigned/<txid>-<int:vout>-<scriptPubKey>-<redeemScript>')
def signed(txid, vout, scriptPubKey, redeemScript):
    return jsonify(createsigned(txid, vout, scriptPubKey, redeemScript))

@app.route('/')
@app.route('/index')
def index():
    return 'hi there!'
