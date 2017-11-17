from openchain.models.exception import BlockchainTreeChildCollisionException, BlockchainTreeParentCollisionException


class BlockchainNode:

    depth = 0

    def __init__(self, item: object, prev_item: object=None, next_item: object=None):
        self.item = item
        self.prev_item = prev_item
        self.next_item = next_item

    def calculate_depth(self):
        if not self.next_item:
            return 0
        return self.next_item.calculate_depth() + 1


class Blockchain:

    block_list = []
    block_tree = {}

    def __init__(self, block_list: list):
        self.block_list = block_list

    def generate_tree(self):
        for block in self.block_list:
            curr_block_node = BlockchainNode(block)

            if block.prev_block in self.block_tree.keys():
                prev_block_node = self.block_tree[block.prev_block]
                if prev_block_node.next_item:
                    raise BlockchainTreeChildCollisionException

                prev_block_node.next_item = curr_block_node
                curr_block_node.prev_item = prev_block_node

            if block.next_block in self.block_tree.keys():
                next_block_node = self.block_tree[block.next_block]
                if next_block_node.prev_item:
                    raise BlockchainTreeParentCollisionException

                next_block_node.prev_item = curr_block_node
                curr_block_node.next_item = next_block_node

            self.block_tree[block.data_hash] = curr_block_node

        for node in self.block_tree.items():
            node.depth = node.calculate_depth()
