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

    def AddOrder(self, order):
        """
        Adds an order to the orderbook.

        :param str order: the order to add
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
