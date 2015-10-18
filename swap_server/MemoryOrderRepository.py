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

    def AddOrder(self, order):
        """
        Adds an order to the orderbook.

        :param str order: the order to add
        :returns: the order identifier
        """
        orderId = self.getOrderId(order)

        if orderId in self.orders:
            raise OrderAlreadyExists

        self.orders[orderId] = order

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

    # TODO: actually check order
