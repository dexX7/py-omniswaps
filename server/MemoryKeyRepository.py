from bitcoinrpc.authproxy import AuthServiceProxy
from KeyRepository import KeyRepository, KeyAlreadyUsed, KeyUnknown, InvalidScript


class MemoryKeyRepository(KeyRepository):

    def __init__(self, rpcServer):
        """Creates a new instance.

        :param AuthServiceProxy rpcServer: the RPC connection
        """
        self.rpc = rpcServer
        self.keysUsed = []
        self.keysUnused = []
        self.keyToHash = {}

    ##
    # Key storage:
    #

    def storePubKey(self, newPubKey, pubKeyHash):
        """Stores a new public key.

        :param str newPubKey:  the public key to store
        :param str pubKeyHash: the corresponding pubkey-hash
        """
        assert not self.isKeyUnused(newPubKey)
        assert not self.isKeyUsed(newPubKey)
        self.keysUnused.append(newPubKey)
        self.keyToHash[newPubKey] = pubKeyHash

    def markKeyDirty(self, usedPubKey):
        """Marks a public key as used.

        :param str usedPubKey: the used public key
        """
        assert self.isKeyUnused(usedPubKey)
        assert not self.isKeyUsed(usedPubKey)
        self.keysUnused.remove(usedPubKey)
        self.keysUsed.append(usedPubKey)

    def isKeyUsed(self, pubKey):
        """Checks whether the public key is unused.

        :param str pubKey: the public key to check
        :returns bool: whether the key was not used before
        """
        return pubKey in self.keysUsed

    def isKeyUnused(self, pubKey):
        """Checks whether the public key is unused.

        :param str pubKey: the public key to check
        :returns bool: whether the key was not used before
        """
        return pubKey in self.keysUnused

    ##
    # Key handling:
    #

    def GetNextPubKey(self):
        """Generates and stores a new key-pair.

        :returns str: an unused public key
        """
        pubKeyHash = self.rpc.getnewaddress()
        keyInfo = self.rpc.validateaddress(pubKeyHash)
        assert keyInfo['isvalid']
        assert keyInfo['address'] == pubKeyHash
        assert 'pubkey' in keyInfo
        pubKey = keyInfo['pubkey']
        self.storePubKey(pubKey, pubKeyHash)
        return pubKey

    ##
    # Signing:
    #

    def SignTransaction(self, rawTx, vIns, sigHashType, signingKey):
        """Signs a raw transaction.

        :param str  rawTx:       the raw transaction to sign
        :param list vIns:        the transaction inputs, including scriptPubKey and redeemScript
        :param str  sigHashType: the signature hash type
        :param str  signingKey:  the key used to sign the transaction
        :returns: the signed raw transaction
        """
        if self.isKeyUsed(signingKey):
            raise KeyAlreadyUsed()
        if not self.isKeyUnused(signingKey):
            raise KeyUnknown()
        if not self.checkTx(rawTx, vIns, signingKey):
            raise InvalidScript()
        self.markKeyDirty(signingKey)
        privKey = self.retrieveKey(signingKey)
        result = self.rpc.signrawtransaction(rawTx, vIns, [privKey], sigHashType)
        assert 'hex' in result
        assert 'complete' in result
        return result['hex'], result['complete']

    def retrieveKey(self, pubKey):
        """Retrieves a private key corresponding to the given public key.

        :param str pubKey: the public key for the key lookup
        :return str: the corresponding private key
        """
        assert pubKey in self.keyToHash
        pubKeyHash = self.keyToHash[pubKey]
        privKey = self.rpc.dumpprivkey(pubKeyHash)
        return privKey

    def checkTx(self, rawTx, vIns, pubKey):
        """Verifies transaction and scripts.

        :param str  rawTx:  the raw transaction to sign
        :param list vIns:   the transaction inputs, including scriptPubKey and redeemScript
        :param str  pubKey: the key going to be used
        :returns bool: whether transaction should be signed
        """
        try:
            tx = self.rpc.decoderawtransaction(rawTx)
        except:
            print('1. decoderawtransaction failed')
            return False

        if len(tx['vin']) != len(vIns):
            print('2. vin size mismatch')
            return False

        for vin in vIns:
            if 'txid' not in vin:
                print('3. txid missing')
                return False

            if 'vout' not in vin:
                print('4. vout missing')
                return False

            if 'scriptPubKey' not in vin:
                print('5. scriptPubKey missing')
                return False

            if 'redeemScript' not in vin:
                print('6. redeemScript missing')
                return False

            redeemScript = vin['redeemScript']
            try:
                script = self.rpc.decodescript(redeemScript)
            except:
                print('7. decodescript failed')
                return False

            if script['type'] != 'multisig':
                print('8. redeemScript is not multisig')
                return False

            if 'reqSigs' not in script:
                print('9. malformed multisig script')
                return False

            asm = script['asm'].split(' ')
            reqSigs = int(asm[-2])
            if reqSigs != int(script['reqSigs']):
                print('10. no full control')
                return False

            if pubKey not in script['asm']:
                print('11. pubKey not as destination')
                return False

        print('checkTx passed')
        return True
