

class KeyAlreadyUsed(Exception):
    def __init__(self):
        pass


class KeyUnknown(Exception):
    def __init__(self):
        pass


class InvalidScript(Exception):
    def __init__(self):
        pass


class KeyRepository:

    def GetNextPubKey(self):
        """
        Generates and stores a new key-pair.

        :returns: the public key corresponding to the new key
        """
        return NotImplemented

    def SignTransaction(self, rawTx, vIns, sigHashType, signingKey):
        """
        Signs a raw transaction.

        :param rawTx:       the raw transaction to sign
        :param vIns:        the transaction inputs, including scriptPubKey and redeemScript
        :param sigHashType: the signature hash type
        :param signingKey:  the key used to sign the transaction
        :returns: the signed raw transaction
        """
        return NotImplemented
