class ModelFactory:

    @staticmethod
    def get_model(name):
        from openchain.models.block import Block
        from openchain.models.blockchain import Blockchain
        from openchain.models.client import Client
        from openchain.models.transaction import Transaction
        from openchain.models.wallet import Wallet

        model_map = {
            'block': Block,
            'blockchain': Blockchain,
            'client': Client,
            'transaction': Transaction,
            'wallet': Wallet,
        }

        if name in model_map:
            return model_map[name]
        return None


class BlockchainFactory:

    @staticmethod
    def build_blockchain(block_list, genesis_block_hash: str=None):
        blockchain = ModelFactory.get_model('blockchain')(block_list)
        blockchain.build(raise_exception=False,
                         genesis_block_hash=genesis_block_hash)
        return blockchain
