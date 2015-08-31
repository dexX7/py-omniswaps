import requests
import config

def request_shared(pubkey):
    r = requests.get('%s/createshared/%s' % (config.API_ENDPOINT, pubkey))
    return r.json()

def request_signed(txid, vout, scriptPubKey, redeemScript):
    print("txid"+txid)
    print("vout"+str(vout))
    print("scriptPubKey"+str(scriptPubKey))
    print("redeemScript"+str(redeemScript))
    r = requests.get('%s/createsigned/%s-%d-%s-%s' % (
        config.API_ENDPOINT, txid, vout, scriptPubKey, redeemScript))
    print(r.text)
    return r.json()
