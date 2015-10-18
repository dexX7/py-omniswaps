class OrderAlreadyExists(Exception):
    def __init__(self):
        pass


class OrderNotFound(Exception):
    def __init__(self):
        pass


class OrderRepository:

    def GetOrder(self, orderId):
        """
        Returns information about an order.

        :param str orderId: the order identifier
        :returns: the order
        """
        return NotImplemented

    def ListOrders(self):
        """
        Returns a list of orders.

        :returns: the orders
        """
        return NotImplemented

    def AddOrder(self, rawTx, prevTxs):
        """
        Adds an order to the orderbook.

        :param str rawTx: the order to add
        :param obj prevTxs: the transaction inputs
        :returns: the order identifier
        """
        return NotImplemented

    def RemoveOrder(self, orderId):
        """
        Removes an order to the orderbook.

        :param str orderId: the order identifier
        :returns: True, if the order was removed successfully
        """
        return NotImplemented
