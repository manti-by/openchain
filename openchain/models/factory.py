class ModelFactory:

    @staticmethod
    def get_model(name):
        from openchain.models.client import Client
        from openchain.models.logentry import LogEntry

        map = {
            'client': Client,
            'logentry': LogEntry,
        }

        if name in map:
            return map[name]
        return None
