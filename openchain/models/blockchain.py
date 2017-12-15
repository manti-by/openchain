import collections

from openchain.models.exception import BlockchainTreeChildCollisionException, BlockchainTreeParentCollisionException


class BlockchainNode:

    block = None
    prev_item = None
    next_item = None
    depth = 0

    def __init__(self, block: callable, prev_item: callable=None, next_item: callable=None):
        self.block = block
        self.prev_item = prev_item
        self.next_item = next_item
        self.depth = 0

    @property
    def __dict__(self):
        unordered = {
            'block': self.block.__dict__,
            'prev_item': self.prev_item.block.data_hash if self.prev_item else None,
            'next_item': self.next_item.block.data_hash if self.next_item else None,
        }
        return collections.OrderedDict(sorted(unordered.items()))

    def calculate_depth(self) -> int:
        if not self.next_item:
            return 0
        return self.next_item.calculate_depth() + 1


class Blockchain:

    collisions = []
    block_tree = {}
    block_list = []

    def __init__(self, block_list: list):
        self.collisions = []
        self.block_tree = {}
        self.block_list = block_list

    @property
    def is_valid(self) -> bool:
        return len(self.collisions) == 0

    @property
    def __dict__(self):
        result = {}
        for block_hash, block in self.block_tree.items():
            result[block_hash] = block.__dict__
        return result

    @property
    def last_block_hash(self):
        try:
            block_hash = next(iter(self.block_tree))
            return self.get_latest_block_hash(block_hash)
        except StopIteration:
            return ''

    def get_latest_block_hash(self, hash):
        if self.block_tree[hash].next_item is None:
            return hash
        else:
            next_hash = self.block_tree[hash].next_item.block.data_hash
            return self.get_latest_block_hash(next_hash)

    def generate_tree(self, raise_exception: bool=True):
        for block in self.block_list:
            curr_block_node = BlockchainNode(block)

            if block.prev_block in self.block_tree:
                prev_block_node = self.block_tree[block.prev_block]
                if prev_block_node.next_item:
                    self.collisions.extend([block, prev_block_node.block])
                    if raise_exception:
                        raise BlockchainTreeChildCollisionException
                    continue

                prev_block_node.next_item = curr_block_node
                curr_block_node.prev_item = prev_block_node

            if block.next_block in self.block_tree:
                next_block_node = self.block_tree[block.next_block]
                if next_block_node.prev_item:
                    self.collisions.extend([block, next_block_node.block])
                    if raise_exception:
                        raise BlockchainTreeParentCollisionException
                    continue

                next_block_node.prev_item = curr_block_node
                curr_block_node.next_item = next_block_node

            self.block_tree[block.data_hash] = curr_block_node

        for key, node in self.block_tree.items():
            node.depth = node.calculate_depth()
