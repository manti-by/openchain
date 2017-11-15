class ModelFactory:

    @staticmethod
    def get_model(name):
        from openchain.models.client import Client
        from openchain.models.logentry import LogEntry
        from openchain.models.transaction import Transaction
        from openchain.models.wallet import Wallet

        map = {
            'client': Client,
            'logentry': LogEntry,
            'transaction': Transaction,
            'wallet': Wallet,
        }

        if name in map:
            return map[name]
        return None
