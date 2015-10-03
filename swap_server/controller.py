from bitcoinrpc.authproxy import AuthServiceProxy
from MemoryKeyRepository import MemoryKeyRepository
import config


class Controller:
    def __init__(self):
        rpcServer = AuthServiceProxy(
            'http://%s:%s@%s:%d' % (config.RPC_USER, config.RPC_PASSWORD, config.RPC_CONNECT, config.RPC_PORT))
        self.repository = MemoryKeyRepository(rpcServer)

    def GetNextPubKey(self):
        return self.repository.GetNextPubKey()

    def Sign(self, rawTx, vIns, sigHashType, signingKey):
        return self.repository.SignTransaction(rawTx, vIns, sigHashType, signingKey)
