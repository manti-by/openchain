from unittest import TestCase

from openchain.models.block import Block
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

    def setUp(self):
        self.dict_list = [
            {'data_hash': 'hash-01', 'prev_block': None, 'next_block': 'hash-02'},
            {'data_hash': 'hash-02', 'prev_block': 'hash-01', 'next_block': 'hash-03'},
            {'data_hash': 'hash-03', 'prev_block': 'hash-02', 'next_block': 'hash-04'},
            {'data_hash': 'hash-04', 'prev_block': 'hash-03', 'next_block': 'hash-05'},
            {'data_hash': 'hash-05', 'prev_block': 'hash-04', 'next_block': None}
        ]

    @property
    def block_list(self):
        result = []
        for data in self.dict_list:
            result.append(Block(**data))
        return result

    def test_blockchain_generation(self):
        blockchain = Blockchain(self.block_list)
        blockchain.generate_tree()
        self.assertEqual(len(blockchain.block_tree.keys()), 5)

    def test_blockchain_generation_with_disordered_transactions(self):
        self.dict_list += [
            {'data_hash': 'hash-06', 'prev_block': 'hash-07', 'next_block': None},
            {'data_hash': 'hash-07', 'prev_block': 'hash-05', 'next_block': 'hash-06'}
        ]
        blockchain = Blockchain(self.block_list)
        blockchain.generate_tree()
        self.assertEqual(len(blockchain.block_tree.keys()), 7)

    def test_blockchain_raise_child_exception(self):
        self.dict_list += [
            {'data_hash': 'hash-06', 'prev_block': 'hash-04', 'next_block': None}
        ]
        blockchain = Blockchain(self.block_list)
        with self.assertRaises(BlockchainTreeChildCollisionException):
            blockchain.generate_tree()
        self.assertFalse(blockchain.is_valid)

    def test_blockchain_raise_parent_exception(self):
        self.dict_list += [
            {'data_hash': 'hash-06', 'prev_block': None, 'next_block': 'hash-05'}
        ]
        blockchain = Blockchain(self.block_list)
        with self.assertRaises(BlockchainTreeParentCollisionException):
            blockchain.generate_tree()
        self.assertFalse(blockchain.is_valid)

    def test_blockchain_last_block_hash(self):
        blockchain = Blockchain(self.block_list)
        blockchain.generate_tree()
        self.assertEqual(blockchain.last_block_hash, 'hash-05')
