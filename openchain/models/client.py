import collections
import time

from openchain.models.base import Model, Manager


class ClientManager(Manager):

    def append(self, item: object, commit: bool=False):
        updated = False
        for c in self.get():
            if item.client_id == c.client_id:
                updated = True
                item.timestamp = time.time()
        if not updated:
            self.queryset.append(item)
        self.save()


class Client(Model):

    client_id = None
    timestamp = None

    objects = ClientManager()

    def __init__(self, client_id: str, timestamp: float=None):
        self.client_id = client_id
        if timestamp is None:
            self.timestamp = time.time()

    @property
    def __dict__(self):
        unordered = {
            'client_id': self.client_id,
            'timestamp': self.timestamp
        }
        return collections.OrderedDict(sorted(unordered.items()))
