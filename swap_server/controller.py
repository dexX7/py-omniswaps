from MemoryOrderRepository import MemoryOrderRepository
from bitcoinrpc.authproxy import AuthServiceProxy
from MemoryKeyRepository import MemoryKeyRepository
import config


class Controller:
    def __init__(self):
        rpcServer = AuthServiceProxy(
            'http://%s:%s@%s:%d' % (config.RPC_USER, config.RPC_PASSWORD, config.RPC_CONNECT, config.RPC_PORT))
        self.keys = MemoryKeyRepository(rpcServer)
        self.orders = MemoryOrderRepository(rpcServer)

    def GetNextPubKey(self):
        return self.keys.GetNextPubKey()

    def Sign(self, rawTx, vIns, sigHashType, signingKey):
        return self.keys.SignTransaction(rawTx, vIns, sigHashType, signingKey)

    def GetOrder(self, orderId):
        return self.orders.GetOrder(orderId)

    def ListOrders(self):
        return self.orders.ListOrders()

    def AddOrder(self, order):
        return self.orders.AddOrder(order)

    def RemoveOrder(self, orderId):
        return self.orders.RemoveOrder(orderId)

    def resetRepositories(self):
        rpcServer = AuthServiceProxy(
            'http://%s:%s@%s:%d' % (config.RPC_USER, config.RPC_PASSWORD, config.RPC_CONNECT, config.RPC_PORT))
        self.keys = MemoryKeyRepository(rpcServer)
        self.orders = MemoryOrderRepository(rpcServer)
