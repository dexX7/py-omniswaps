from bitcoinrpc.authproxy import AuthServiceProxy
from OrderRepository import OrderRepository, OrderNotFound, OrderAlreadyExists


class MemoryOrderRepository(OrderRepository):

    def __init__(self, rpcServer):
        """Creates a new instance.

        :param AuthServiceProxy rpcServer: the RPC connection
        """
        self.rpc = rpcServer
        self.orders = {}

    def GetOrder(self, orderId):
        """
        Returns information about an order.

        :param str orderId: the order identifier
        :returns: the order
        """
        if orderId not in self.orders:
            raise OrderNotFound

        return self.orders[orderId]

    def ListOrders(self):
        """
        Returns a list of orders.

        :returns: the orders
        """
        return self.orders

    def AddOrder(self, rawTx, prevTxs):
        """
        Adds an order to the orderbook.

        :param str rawTx: the order to add
        :param obj prevTxs: the transaction inputs
        :returns: the order identifier
        """
        orderId = self.getOrderId(rawTx)

        if orderId in self.orders:
            raise OrderAlreadyExists

        self.orders[orderId] = self.makeOrder(rawTx, prevTxs)

        return orderId

    def RemoveOrder(self, orderId):
        """
        Removes an order to the orderbook.

        :param str orderId: the order identifier
        :returns: True, if the order was removed successfully
        """
        if orderId not in self.orders:
            raise OrderNotFound

        del self.orders[orderId]

        return True

    def getOrderId(self, order):
        decoded = self.rpc.decoderawtransaction(order)  # TODO: catch failure

        return decoded['txid']

    @staticmethod
    def makeOrder(rawTx, prevTxs):
        return {
            'rawtx': rawTx,
            'prevtxs': prevTxs
        }

    # TODO: actually check order
