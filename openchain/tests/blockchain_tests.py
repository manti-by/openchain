from unittest import TestCase

from openchain.models.blockchain import Blockchain, BlockchainNode
from openchain.models.exception import BlockchainTreeChildCollisionException, BlockchainTreeParentCollisionException


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


class BlockchainTestCase(TestCase):

    block_list = [
        {'hash-01': {'prev_block': None, 'next_block': 'hash-02'}},
        {'hash-02': {'prev_block': 'hash-01', 'next_block': 'hash-03'}},
        {'hash-03': {'prev_block': 'hash-02', 'next_block': 'hash-04'}},
        {'hash-04': {'prev_block': 'hash-03', 'next_block': 'hash-05'}},
        {'hash-05': {'prev_block': 'hash-04', 'next_block': None}}
    ]

    def test_blockchain_generation(self):
        blockchain = Blockchain(self.block_list)
        blockchain.generate_tree()
        self.assertEqual(len(blockchain.block_tree.keys()), 5)

    def test_blockchain_generation_with_disordered_transactions(self):
        disordered_block_list = self.block_list + [
            {'hash-06': {'prev_block': 'hash-07', 'next_block': None}},
            {'hash-07': {'prev_block': 'hash-05', 'next_block': 'hash-06'}}
        ]
        blockchain = Blockchain(disordered_block_list)
        blockchain.generate_tree()
        self.assertEqual(len(blockchain.block_tree.keys()), 7)

    def test_blockchain_raise_child_exception(self):
        invalid_block_list = self.block_list + [{'hash-06': {'prev_block': 'hash-04', 'next_block': None}}]
        blockchain = Blockchain(invalid_block_list)
        with self.assertRaises(BlockchainTreeChildCollisionException):
            blockchain.generate_tree()
        self.assertFalse(blockchain.is_valid)

    def test_blockchain_raise_parent_exception(self):
        invalid_block_list = self.block_list + [{'hash-06': {'prev_block': None, 'next_block': 'hash-05'}}]
        blockchain = Blockchain(invalid_block_list)
        with self.assertRaises(BlockchainTreeParentCollisionException):
            blockchain.generate_tree()
        self.assertFalse(blockchain.is_valid)
