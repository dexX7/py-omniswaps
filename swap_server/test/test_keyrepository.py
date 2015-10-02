import unittest
from KeyRepository import KeyAlreadyUsed, KeyUnknown, InvalidScript
from bitcoinrpc.authproxy import AuthServiceProxy
from MemoryKeyRepository import MemoryKeyRepository
import config


class TestMemoryKeyRepository(unittest.TestCase):
    def setUp(self):
        self.rpcServer = AuthServiceProxy('http://%s:%s@%s:%d' % (
            config.RPC_USER, config.RPC_PASSWORD, config.RPC_CONNECT, config.RPC_PORT))

        self.repository = MemoryKeyRepository(self.rpcServer)

    def test_Help(self):
        self.assertIsNotNone(self.rpcServer.help())

    def test_KeyGeneration(self):
        key1 = self.repository.GetNextPubKey()
        key2 = self.repository.GetNextPubKey()
        key3 = self.repository.GetNextPubKey()
        self.assertIsNotNone(key1)
        self.assertIsNotNone(key2)
        self.assertIsNotNone(key3)
        self.assertNotEqual(key1, key2)
        self.assertNotEqual(key2, key3)

    def test_SignDummy(self):
        rawTx = '01000000000000000000'
        vIns = {}
        sigHashType = 'ALL'
        signingKey = self.repository.GetNextPubKey()

        result, complete = self.repository.SignTransaction(rawTx, vIns, sigHashType, signingKey)
        self.assertIsNotNone(result)
        self.assertTrue(complete)

    def test_SignKeyAlreadyUsed(self):
        rawTx = '01000000000000000000'
        vIns = {}
        sigHashType = 'ALL'
        signingKey = self.repository.GetNextPubKey()

        self.repository.SignTransaction(rawTx, vIns, sigHashType, signingKey)  # doesn't throw
        with self.assertRaises(KeyAlreadyUsed):
            self.repository.SignTransaction(rawTx, vIns, sigHashType, signingKey)

    def test_SignUnknownKey(self):
        rawTx = '01000000000000000000'
        vIns = {}
        sigHashType = 'ALL'
        signingKey = '038306828cc42bdfebb2c6d82ed7a737e5cf49cad7588bfda880aef2dc03979ea6'

        with self.assertRaises(KeyUnknown):
            self.repository.SignTransaction(rawTx, vIns, sigHashType, signingKey)

    def test_SignInvalidScript(self):
        rawTx = '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000'
        vIns = [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76', 'vout': 5}]
        sigHashType = 'ALL'
        signingKey = self.repository.GetNextPubKey()

        with self.assertRaises(InvalidScript):
            self.repository.SignTransaction(rawTx, vIns, sigHashType, signingKey)

    def test_ValidTxCheck(self):
        self.assertTrue(self.repository.checkTx(
            '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000',
            [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76',
              'vout': 0,
              'scriptPubKey': 'a91452e8dcf54b62f73930456d2dccfc668821262ca587',
              'redeemScript': '522102eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9210300c2fe7e8816ea'
                              '4722bcc42a13137da688239421a28006f365ba92875ad8e65e52ae'}],
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

    def test_InvalidTxCheck(self):
        # malformed hex
        self.assertFalse(self.repository.checkTx(
            '0100000000000000000',
            {},
            '038306828cc42bdfebb2c6d82ed7a737e5cf49cad7588bfda880aef2dc03979ea6'))

        # vIns size mismatch
        self.assertFalse(self.repository.checkTx(
            '01000000016fc887ac32de1e24dc9e8a7a0f3ba39f351b732dac72428202994c42c0c26e020000000000ffffffff0000000000',
            {},
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

        # tx.vIns size mismatch
        self.assertFalse(self.repository.checkTx(
            '01000000000000000000',
            [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76',
              'vout': 0,
              'scriptPubKey': 'a91452e8dcf54b62f73930456d2dccfc668821262ca587',
              'redeemScript': '522102eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9210300c2fe7e8816ea'
                              '4722bcc42a13137da688239421a28006f365ba92875ad8e65e52ae'}],
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

        # txid missing
        self.assertFalse(self.repository.checkTx(
            '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000',
            [{'vout': 0,
              'scriptPubKey': 'a91452e8dcf54b62f73930456d2dccfc668821262ca587',
              'redeemScript': '522102eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9210300c2fe7e8816ea'
                              '4722bcc42a13137da688239421a28006f365ba92875ad8e65e52ae'}],
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

        # vout missing
        self.assertFalse(self.repository.checkTx(
            '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000',
            [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76',
              'scriptPubKey': 'a91452e8dcf54b62f73930456d2dccfc668821262ca587',
              'redeemScript': '522102eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9210300c2fe7e8816ea'
                              '4722bcc42a13137da688239421a28006f365ba92875ad8e65e52ae'}],
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

        # scriptPubKey missing
        self.assertFalse(self.repository.checkTx(
            '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000',
            [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76',
              'vout': 0,
              'redeemScript': '522102eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9210300c2fe7e8816ea'
                              '4722bcc42a13137da688239421a28006f365ba92875ad8e65e52ae'}],
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

        # redeemScript missing
        self.assertFalse(self.repository.checkTx(
            '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000',
            [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76',
              'vout': 0,
              'scriptPubKey': 'a91452e8dcf54b62f73930456d2dccfc668821262ca587'}],
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

        # invalid redeemScript
        self.assertFalse(self.repository.checkTx(
            '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000',
            [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76',
              'vout': 0,
              'scriptPubKey': 'a91452e8dcf54b62f73930456d2dccfc668821262ca587',
              'redeemScript': '007'}],
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

        # no multisig script
        self.assertFalse(self.repository.checkTx(
            '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000',
            [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76',
              'vout': 0,
              'scriptPubKey': 'a91452e8dcf54b62f73930456d2dccfc668821262ca587',
              'redeemScript': 'a9149ab70a63e9f3a597e7b32a04a0107466c8dfb04887'}],
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

        # malformed multisig script
        self.assertFalse(self.repository.checkTx(
            '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000',
            [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76',
              'vout': 0,
              'scriptPubKey': 'a91452e8dcf54b62f73930456d2dccfc668821262ca587',
              'redeemScript': '532102eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9210300c2fe7e8816ea'
                              '4722bcc42a13137da688239421a28006f365ba92875ad8e65e52ae'}],
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

        # no full control
        self.assertFalse(self.repository.checkTx(
            '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000',
            [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76',
              'vout': 0,
              'scriptPubKey': 'a91452e8dcf54b62f73930456d2dccfc668821262ca587',
              'redeemScript': '512102eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9210300c2fe7e8816ea'
                              '4722bcc42a13137da688239421a28006f365ba92875ad8e65e52ae'}],
            '02eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9'))

        # pubKey not included
        self.assertFalse(self.repository.checkTx(
            '010000000176fea4d5fda4f24e90de00baf2ea4a030b6b415edc4e49db1b0368be0a7840a60000000000ffffffff0000000000',
            [{'txid': 'a640780abe68031bdb494edc5e416b0b034aeaf2ba00de904ef2a4fdd5a4fe76',
              'vout': 0,
              'scriptPubKey': 'a91452e8dcf54b62f73930456d2dccfc668821262ca587',
              'redeemScript': '522102eaeaf4de1717a5c4dc21ca4de53b82a305dbea8659babb32b3c791f6374639c9210300c2fe7e8816ea'
                              '4722bcc42a13137da688239421a28006f365ba92875ad8e65e52ae'}],
            '03910e30c63e3907cb323f38919ed35216d6263a41096252efcf068dd34c642fd6'))

        # TODO: test successful signing
        # TODO: ensure only the signing key is used!
        # TODO: ensure output wasn't used before!


if __name__ == '__main__':
    unittest.main()
