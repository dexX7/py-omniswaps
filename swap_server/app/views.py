from flask import make_response, jsonify, request
from KeyRepository import KeyAlreadyUsed
from KeyRepository import KeyUnknown
from KeyRepository import InvalidScript
from OrderRepository import OrderNotFound, OrderAlreadyExists
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


##
# Key handling:
#

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


##
# Order handling:
#

@app.route('/getorder/<orderId>')
def getorder(orderId):
    try:
        order = ctrl.GetOrder(orderId)
        result = {'orderId': orderId, 'order': order}
        code = 200

    except OrderNotFound:
        result = {'error': 'order not found'}
        code = 404

    except:
        result = {'error': 'internal server error'}
        code = 500

    return respond(result, code)


@app.route('/getorders')
def getorders():
    try:
        result = ctrl.ListOrders()
        code = 200

    except:
        result = {'error': 'internal server error'}
        code = 500

    return respond(result, code)


@app.route('/addorder', methods=['POST'])
def addorder():
    data = request.get_json()

    if 'order' not in data:
        result = {'error': 'malformed request'}
        code = 400

        return respond(result, code)

    order = data['order']

    try:
        orderId = ctrl.AddOrder(order)
        result = {'orderId': orderId, 'order': order}
        code = 201

    except OrderAlreadyExists:
        result = {'error': 'order already exists'}
        code = 409

    except:
        result = {'error': 'internal server error'}
        code = 500

    return respond(result, code)


@app.route('/removeorder', methods=['POST'])
def removeorder():
    data = request.get_json()

    if 'orderId' not in data:
        result = {'error': 'malformed request'}
        code = 400

        return respond(result, code)

    orderId = data['orderId']

    try:
        status = ctrl.RemoveOrder(orderId)
        result = {'orderId': orderId, 'removed': status}
        code = 200

    except OrderNotFound:
        result = {'error': 'order not found'}
        code = 404

    except:
        result = {'error': 'internal server error'}
        code = 500

    return respond(result, code)


##
# Misc:
#

@app.route('/reset')
def reset():
    try:
        ctrl.resetRepositories()
        result = {'reset': True}
        code = 200

    except:
        result = {'error': 'internal server error'}
        code = 500

    return respond(result, code)


@app.route('/')
@app.route('/index')
def index():
    return 'hello!'
