class ModelFactory:

    @staticmethod
    def get_model(name):
        from openchain.models.block import Block
        from openchain.models.client import Client
        from openchain.models.logentry import LogEntry
        from openchain.models.transaction import Transaction
        from openchain.models.wallet import Wallet

        model_map = {
            'block': Block,
            'client': Client,
            'logentry': LogEntry,
            'transaction': Transaction,
            'wallet': Wallet,
        }

        if name in model_map:
            return model_map[name]
        return None


class BlockchainFactory:

    @staticmethod
    def build_blockchain(block_list):
        from openchain.models.blockchain import Blockchain
        blockchain = Blockchain(block_list)
        blockchain.build(raise_exception=False)
        return blockchain
