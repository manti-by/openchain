import collections
import operator

from typing import Union, List

from openchain.models.block import Block
from openchain.models.exception import (
    BlockchainTreeCollisionException,
    BlockchainInvalidGenesisBlockException
)


class BlockchainNode:

    block = None
    prev_node = None
    next_nodes = []
    depth = 0

    def __init__(self, block: Block, prev_node: 'BlockchainNode'=None,
                 next_nodes: List['BlockchainNode']=None):
        self.block = block
        self.prev_node = prev_node
        if next_nodes is not None:
            self.next_nodes = next_nodes
        self.depth = 0

    @property
    def next_node(self) -> Union['BlockchainNode', None]:
        if not self.next_nodes:
            return None
        return max(self.next_nodes, key=operator.attrgetter('depth'))

    @property
    def __dict__(self) -> dict:
        prev_block = None
        if self.prev_node and self.prev_node.block:
            prev_block = self.prev_node.block.data_hash

        next_block = None
        if self.next_node and self.next_node.block:
            next_block = self.next_node.block.data_hash

        unordered = {
            'block': self.block.__dict__,
            'prev_block': prev_block,
            'next_block': next_block,
        }
        return collections.OrderedDict(sorted(unordered.items()))

    def calculate_depth(self) -> int:
        if self.next_nodes:
            self.depth = max(
                map(lambda x: x.calculate_depth(), self.next_nodes)
            ) + 1
        return self.depth


class Blockchain:

    block_tree = {}
    block_list = []
    is_tree_generated = True

    def __init__(self, block_list: List[Block]):
        self.block_tree = {}
        self.block_list = block_list
        self.is_tree_generated = False

    @property
    def __dict__(self) -> dict:
        result = {}
        for block_hash, block in self.block_tree.items():
            result[block_hash] = block.__dict__
        return result

    @property
    def last_block_hash(self) -> Union[str, None]:
        block_keys = list(self.block_tree.keys())
        return block_keys[-1] if len(block_keys) else None

    def generate_nodes(self, current_block: Block, prev_block: Block=None) -> BlockchainNode:
        next_nodes = []
        for block in self.block_list:
            if block.prev_block == current_block.data_hash:
                next_node = self.generate_nodes(block, current_block)
                if next_node is not None:
                    next_nodes.append(next_node)

        prev_node = BlockchainNode(prev_block)
        return BlockchainNode(current_block, prev_node, next_nodes)

    def generate_tree(self, current_block: BlockchainNode, raise_exception: bool=False):
        if current_block is None:
            return

        self.block_tree[current_block.block.data_hash] = current_block

        if len(current_block.next_nodes) > 1 and raise_exception:
            raise BlockchainTreeCollisionException

        self.generate_tree(current_block.next_node, raise_exception)

    def build(self, raise_exception: bool=True):
        if self.is_tree_generated:
            return

        genesis_block = None
        for genesis_block in self.block_list:
            if genesis_block.is_genesis:
                break

        if genesis_block is None:
            if raise_exception:
                raise BlockchainInvalidGenesisBlockException
            else:
                return

        genesis_node = self.generate_nodes(genesis_block)
        self.generate_tree(genesis_node, raise_exception)

        self.is_tree_generated = True

        for key, node in self.block_tree.items():
            node.depth = node.calculate_depth()

    @property
    def is_valid(self):
        try:
            self.build(True)
            return True
        except BlockchainTreeCollisionException:
            return False

    def can_add_block(self, block: object) -> bool:
        # Store original blockchain tree
        original_block_tree = self.block_tree

        # Store original blockchain tree
        self.block_list.append(block)
        is_valid = self.is_valid

        # Restore original blockchain tree
        self.block_tree = original_block_tree
        return is_valid
