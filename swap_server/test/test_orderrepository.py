import unittest

from MemoryOrderRepository import MemoryOrderRepository
from OrderRepository import OrderAlreadyExists, OrderNotFound
from bitcoinrpc.authproxy import AuthServiceProxy
import config


class TestMemoryKeyRepository(unittest.TestCase):
    def setUp(self):
        self.rpcServer = AuthServiceProxy('http://%s:%s@%s:%d' % (
            config.RPC_USER, config.RPC_PASSWORD, config.RPC_CONNECT, config.RPC_PORT))

    def test_Help(self):
        self.assertIsNotNone(self.rpcServer.help())

    def test_AddOrder(self):
        orderBook = MemoryOrderRepository(self.rpcServer)
        order = self.getTestOrder()

        orderId = orderBook.AddOrder(order['order'])
        self.assertEqual(order['orderId'], orderId)

    def test_AddOrderAlreadyExists(self):
        orderBook = MemoryOrderRepository(self.rpcServer)
        order = self.getTestOrder()

        orderBook.AddOrder(order['order'])
        with self.assertRaises(OrderAlreadyExists):
            orderBook.AddOrder(order['order'])

    def test_GetOrder(self):
        orderBook = MemoryOrderRepository(self.rpcServer)
        order = self.getTestOrder()

        orderId = orderBook.AddOrder(order['order'])
        orderRetrieved = orderBook.GetOrder(orderId)
        self.assertEqual(order['order'], orderRetrieved)

    def test_GetOrderNotFound(self):
        orderBook = MemoryOrderRepository(self.rpcServer)

        orderId = '0000000000000000000000000000000000000000000000000000000000000404'
        with self.assertRaises(OrderNotFound):
            orderBook.GetOrder(orderId)

    def test_RemoveOrder(self):
        orderBook = MemoryOrderRepository(self.rpcServer)
        order = self.getTestOrder()

        orderId = orderBook.AddOrder(order['order'])
        orderRetrieved = orderBook.GetOrder(orderId)
        self.assertEqual(order['order'], orderRetrieved)

        self.assertTrue(orderBook.RemoveOrder(orderId))
        with self.assertRaises(OrderNotFound):
            orderBook.GetOrder(orderId)

    def test_RemoveOrderNotFound(self):
        orderBook = MemoryOrderRepository(self.rpcServer)

        orderId = '0000000000000000000000000000000000000000000000000000000000000404'
        with self.assertRaises(OrderNotFound):
            orderBook.RemoveOrder(orderId)

    def getTestOrder(self):
        orderId = '66f30dd1b38dd1eab53fb3418a8315c26ef84ea3e12bad666862945cf92c8772'
        order = '0100000001d1dc83f036909cfb4fa285aa2c9449ecb8f4112f5705b1882263882c155b6eb301000000da004830450221008f' \
                '17801836021dc67797fe03aff3ef4e1a1c75673ebd2ae273f04103c65c88ba0220212449fa8632604e2e81cecd42fdf3bc27' \
                '5c0af4f75735b77dcfdbade0e69df083473044022005d88f476af7e165b30952c3f24a6c91d8f36e6a2766daabed024f64ee' \
                'ab3c3302207b84e60b2202b07d469eb957a628daf65328db9f6f9b058927bea56145645b7282475221037d65bd0df8669bec' \
                '8d2516ae9e6fd98b5ec12b28fcba9cd100e71586ad8fd37d2103919026a74a653c6f28277097528e935c567027b84621d52c' \
                '6e58e0a9cc33fb9c52aeffffffff0100e1f505000000001976a91401ad66f81d5f4ef6e61ba4c34818de3899bf2e6788ac00' \
                '000000'

        return {'orderId': orderId, 'order': order}


if __name__ == '__main__':
    unittest.main()
