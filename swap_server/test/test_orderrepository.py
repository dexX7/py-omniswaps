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

        orderId = orderBook.AddOrder(order['hex'], order['prevtxs'])
        self.assertEqual(order['id'], orderId)

    def test_AddOrderAlreadyExists(self):
        orderBook = MemoryOrderRepository(self.rpcServer)
        order = self.getTestOrder()

        orderBook.AddOrder(order['hex'], order['prevtxs'])
        with self.assertRaises(OrderAlreadyExists):
            orderBook.AddOrder(order['hex'], order['prevtxs'])

    def test_GetOrder(self):
        orderBook = MemoryOrderRepository(self.rpcServer)
        order = self.getTestOrder()

        orderId = orderBook.AddOrder(order['hex'], order['prevtxs'])
        orderRetrieved = orderBook.GetOrder(orderId)
        self.assertEqual(order['hex'], orderRetrieved['hex'])
        self.assertEqual(order['prevtxs'], orderRetrieved['prevtxs'])

    def test_GetOrderNotFound(self):
        orderBook = MemoryOrderRepository(self.rpcServer)

        orderId = '0000000000000000000000000000000000000000000000000000000000000404'
        with self.assertRaises(OrderNotFound):
            orderBook.GetOrder(orderId)

    def test_ListOrdersEmpty(self):
        orderBook = MemoryOrderRepository(self.rpcServer)

        orders = orderBook.ListOrders()
        self.assertEqual(0, len(orders))

    def test_ListOrders(self):
        orderBook = MemoryOrderRepository(self.rpcServer)
        order = self.getTestOrder()

        orderId = orderBook.AddOrder(order['hex'], order['prevtxs'])
        orders = orderBook.ListOrders()
        self.assertEqual(1, len(orders))
        self.assertIn(orderId, orders)

    def test_RemoveOrder(self):
        orderBook = MemoryOrderRepository(self.rpcServer)
        order = self.getTestOrder()

        orderId = orderBook.AddOrder(order['hex'], order['prevtxs'])
        orderRetrieved = orderBook.GetOrder(orderId)
        self.assertEqual(order['hex'], orderRetrieved['hex'])
        self.assertEqual(order['prevtxs'], orderRetrieved['prevtxs'])

        self.assertTrue(orderBook.RemoveOrder(orderId))
        with self.assertRaises(OrderNotFound):
            orderBook.GetOrder(orderId)

    def test_RemoveOrderNotFound(self):
        orderBook = MemoryOrderRepository(self.rpcServer)

        orderId = '0000000000000000000000000000000000000000000000000000000000000404'
        with self.assertRaises(OrderNotFound):
            orderBook.RemoveOrder(orderId)

    def getTestOrder(self):
        orderId = '3d9c7c0925ca1b127b4fe5e3a2d9ed1fe83c012ffa2e164703eed8ec7b3f443e'
        orderTx = '0100000001c14dc37264f069921d4b268fbd866d60afbe5394696750661e75543657cf527d01000000da00483045022100' \
                  'bbeb5ebb9c55c85e940b9a09b32866db707ce81660df4d3531e160058fb1bfc5022025eb910934c4a7726d95d0286fd08d' \
                  '4ce3d4261d3be9189b1d211ddb1aefd76982473044022032ee848b0c11e66c898ba9136a6b094fa235bd8e37ca5abf63e7' \
                  '51790b10bc43022065f20e84a4bc6f0f4392a9fdccdedf7919280774f76e8606ce1709dc609cfbf2834752210264d720ad' \
                  'bc4f59737dff2961c9fd94df94652b13636bd68e1996e28bf2a15afd2103ad4bb225c401c645fffad95679dd0f8d3fab1f' \
                  'b24a59f81c30299d807312584752aeffffffff0100e1f505000000001976a91401ad66f81d5f4ef6e61ba4c34818de3899' \
                  'bf2e6788ac00000000'
        prevTxs = [{
            'txid': '7d52cf573654751e665067699453beaf606d86bd8f264b1d9269f06472c34dc1',
            'vout': 1,
            'scriptPubKey': 'a914cf91f8438874f5e0dc1ade63b97210472c494d5d87',
            'redeemScript': '52210264d720adbc4f59737dff2961c9fd94df94652b13636bd68e1996e28bf2a15afd2103ad4bb225c401c645'
                            'fffad95679dd0f8d3fab1fb24a59f81c30299d807312584752ae'
          }]

        return {'id': orderId, 'hex': orderTx, 'prevtxs': prevTxs}


if __name__ == '__main__':
    unittest.main()
