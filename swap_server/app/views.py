from flask import make_response, jsonify, request
from KeyRepository import KeyAlreadyUsed
from KeyRepository import KeyUnknown
from KeyRepository import InvalidScript
from app import app
from controller import Controller

ctrl = Controller()


def respond(result, code):
    app.logger.info(result)

    return make_response(jsonify(result), code)


@app.errorhandler(404)
def not_found_error(error):
    result = {'error': 'not found'}
    code = 404

    return respond(result, code)


@app.errorhandler(500)
def internal_error(error):
    result = {'error': 'internal server error'}
    code = 500

    return respond(result, code)


@app.route('/getpubkey')
def getpubkey():
    try:
        pubKey = ctrl.GetNextPubKey()
        result = {'pubkey': pubKey}
        code = 200

    except:
        result = {'error': 'internal server error'}
        code = 500

    return respond(result, code)


@app.route('/sign', methods=['POST'])
def sign():
    data = request.get_json()

    if 'rawtx' not in data or 'prevtxs' not in data or 'sighashtype' not in data or 'key' not in data:
        result = {'error': 'malformed request'}
        code = 400

        return respond(result, code)

    rawTx = data['rawtx']
    prevTxs = data['prevtxs']
    sigHashType = data['sighashtype']
    signingKey = data['key']

    try:
        signedTx, complete = ctrl.Sign(rawTx, prevTxs, sigHashType, signingKey)
        result = {'hex': signedTx, 'complete': complete}
        code = 200

    except KeyAlreadyUsed:
        result = {'error': 'key already used'}
        code = 403

    except KeyUnknown:
        result = {'error': 'unknown key'}
        code = 403

    except InvalidScript:
        result = {'error': 'invalid request'}
        code = 403

    except:
        result = {'error': 'internal server error'}
        code = 500

    return respond(result, code)


@app.route('/')
@app.route('/index')
def index():
    return 'hello!'
