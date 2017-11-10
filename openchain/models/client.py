import time

from openchain.models.base import Model, Manager


class ClientManager(Manager):

    def append(self, client: object, commit: bool=False):
        updated = False
        for c in self.get():
            if client == c:
                updated = True
                client.timestamp = time.time()
        if not updated:
            self.qs.append(client)
        self.save()

    def model_from_dict(self, data):
        return Client(**data)


class Client(Model):

    client_id = None
    timestamp = None

    objects = ClientManager

    def __init__(self, client_id: str, timestamp: float=None):
        self.client_id = client_id
        if timestamp is None:
            self.timestamp = time.time()

    @property
    def __dict__(self):
        return {
            'client_id': self.client_id,
            'timestamp': self.timestamp
        }
