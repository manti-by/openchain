# @TODO: Replace this hack for circular imports
import sys


class ModelFactory:

    @staticmethod
    def get_model(name):
        try:
            from openchain.models.client import Client
        except ImportError:
            Client = sys.modules[__package__ + '.client.Client']

        try:
            from openchain.models.logentry import LogEntry
        except ImportError:

            LogEntry = sys.modules[__package__ + '.logentry.LogEntry']

        map = {
            'clientmanager': Client,
            'logentrymanager': LogEntry,
        }

        if name in map:
            return map[name]
        return None
