import time

from openchain.models.base import Model, Manager


class LogEntryManager(Manager):

    def model_from_dict(self, data):
        return LogEntry(**data)


class LogEntry(Model):

    message = None
    timestamp = None

    objects = LogEntryManager

    def __init__(self, message: str, timestamp: float=None):
        self.message = message
        if timestamp is None:
            self.timestamp = time.time()

    @property
    def __dict__(self):
        return {
            'message': self.message,
            'timestamp': self.timestamp
        }
