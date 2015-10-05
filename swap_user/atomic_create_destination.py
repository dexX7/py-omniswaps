import simplejson
import sys
from server import *
from api import request_pubkey, request_sign

def CreatePubKey():
    """
    Creates a new key pair for the user.
    """
    pubKeyHash = getnewaddress()
    result = validateaddress(pubKeyHash)
    return result['pubkey']


def CreateMultisig(pubKeys):
    """
    Creates a multisig script destination with the given keys.
    """
    pubKeys = sorted(pubKeys)
    responseCreate = createmultisig(len(pubKeys), pubKeys)
    responseScript = decodescript(responseCreate['redeemScript'])
    addmultisigaddress(len(pubKeys), pubKeys)
    result = {
        'address': responseScript['p2sh'],
        'pubkeys': pubKeys,
        'redeemScript': responseCreate['redeemScript'],
        'reqSigs': responseScript['reqSigs'],
        'type': responseScript['type'],
    }
    return result


def CreateDestination(pubKeyUser):
    """
    Creates a script locked 2-of-2 multisig destination.
    """
    responsePK = request_pubkey()
    pubKeyServer = responsePK['pubkey']
    print('public key user:   %s' % pubKeyUser)
    print('public key server: %s' % pubKeyServer)
    return CreateMultisig([pubKeyUser, pubKeyServer])


#rawTx = '01000000000000000000'
#prevTxs = []
#sigHashType = 'NONE|ANYONECANPAY'
#signingKey = responsePK['pubkey']

#responseSign = request_sign(rawTx, prevTxs, sigHashType, signingKey)
#print(responseSign)

def print_json(parsed):
    print(simplejson.dumps(parsed, indent=2))


def help():
    print("atomic_create_destination pubkey\n")
    print("Creates script locked 2-of-2 multisig destination.\n")
    print("Arguments:")
    print("1. pubkey    (string, optional) the user's public key\n")
    print("Examples:")
    print("atomic_create_destination")
    print("atomic_create_destination 032c6d9e8c65b62b4f8e8396a7687830590fad2a4bebde5d6be5b7d3d9f0019cc1")
    exit()


def main():
    if len(sys.argv) < 1 or len(sys.argv) > 2 or str(sys.argv[1]) == 'help':
        help()

    pubKey = ''
    if len(sys.argv) > 1:
        pubKey = str(sys.argv[1])
    else:
        pubKey = CreatePubKey()

    result = CreateDestination(pubKey)
    print_json(result)


if __name__ == "__main__":
    main()
