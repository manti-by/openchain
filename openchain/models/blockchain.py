from openchain.models.exception import BlockchainTreeChildCollisionException, BlockchainTreeParentCollisionException


class BlockchainNode:

    depth = 0

    def __init__(self, block: callable, prev_item: callable=None, next_item: callable=None):
        self.block = block
        self.prev_item = prev_item
        self.next_item = next_item

    def calculate_depth(self) -> int:
        if not self.next_item:
            return 0
        return self.next_item.calculate_depth() + 1


class Blockchain:

    def __init__(self, block_list: list):
        self.collisions = []
        self.block_tree = {}
        self.block_list = block_list

    @property
    def is_valid(self) -> bool:
        return len(self.collisions) == 0

    def generate_tree(self, raise_exception: bool=True):
        for block in self.block_list:
            block_hash = next(iter(block))
            block_data = next(iter(block.values()))
            curr_block_node = BlockchainNode(block)

            if block_data['prev_block'] in self.block_tree.keys():
                prev_block_node = self.block_tree[block_data['prev_block']]
                if prev_block_node.next_item:
                    self.collisions.extend([block, prev_block_node.block])
                    if raise_exception:
                        raise BlockchainTreeChildCollisionException

                prev_block_node.next_item = curr_block_node
                curr_block_node.prev_item = prev_block_node

            if block_data['next_block'] in self.block_tree.keys():
                next_block_node = self.block_tree[block_data['next_block']]
                if next_block_node.prev_item:
                    self.collisions.extend([block, next_block_node.block])
                    if raise_exception:
                        raise BlockchainTreeParentCollisionException

                next_block_node.prev_item = curr_block_node
                curr_block_node.next_item = next_block_node

            self.block_tree[block_hash] = curr_block_node

        for key, node in self.block_tree.items():
            node.depth = node.calculate_depth()
