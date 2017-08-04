import time
import json

from app.utils import string_to_bytes


class ClientManager(object):

    clients = []

    def __init__(self, data):
        for client in json.loads(data.decode()):
            self.clients.append(Client(**client))

    def __bytes__(self):
        return string_to_bytes(self.__str__())

    def __str__(self):
        return '[%s]' % ', '.join([c.__str__() for c in self.clients])

    def update_client(self, client_id):
        updated = False
        for client in self.clients:
            if client.client_id == client_id:
                updated = True
                client.timestamp = time.time()
        if not updated:
            self.clients.append(Client(client_id))


class Client(object):

    client_id = None
    timestamp = None

    def __init__(self, client_id, timestamp=None):
        self.client_id = client_id
        self.timestamp = timestamp if isinstance(timestamp, float) else time.time()

    def __bytes__(self):
        return string_to_bytes(self.__str__())

    def __str__(self):
        return '{"client_id": "%s", "timestamp": %f}' % (self.client_id, self.timestamp)
