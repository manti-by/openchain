from unittest import TestCase

from openchain.models.blockchain import BlockchainNode


class BlockchainNodeTestCase(TestCase):

    def test_blockchain_node(self):
        node = BlockchainNode({})
        node.calculate_depth()
        self.assertEqual(node.depth, 0)

    def test_blockchain_tree(self):
        node_03 = BlockchainNode({})
        node_02 = BlockchainNode({})
        node_01 = BlockchainNode({})

        node_03.prev_item = node_02
        node_02.next_item = node_03
        node_02.prev_item = node_01
        node_01.next_item = node_02

        self.assertEqual(node_01.calculate_depth(), 2)
