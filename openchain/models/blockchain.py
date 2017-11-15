
class BlockchainNode:

    depth = 0

    def __init__(self, item: object, left: object=None, right: object=None):
        self.item = item
        self.left = left
        self.right = right

    def calculate_depth(self):
        left_depth = self.left.calculate_depth() if self.left else 0
        right_depth = self.right.calculate_depth() if self.right else 0
        return max(left_depth, right_depth) + 1


class Blockchain:

    block_list = []
    block_tree = {}

    def __init__(self, block_list: list):
        self.block_list = block_list

    def generate_tree(self):
        for block in self.block_list:
            curr_block_node = BlockchainNode(value=block)

            if block.prev_block in self.block_tree.keys():
                prev_block_node = self.block_tree[block.prev_block]
                prev_block_node.right = curr_block_node
                curr_block_node.left = prev_block_node

            if block.next_block in self.block_tree.keys():
                next_block_node = self.block_tree[block.next_block]
                next_block_node.left = curr_block_node
                curr_block_node.right = next_block_node

            self.block_tree[block.data_hash] = curr_block_node

    def calculate_depth_for_three_nodes(self):
        for node in self.block_tree.items():
            node.depth = node.calculate_depth()
