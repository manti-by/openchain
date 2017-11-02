import time
import logging

from open_blockchain.models.base import Manager
from open_blockchain.utils import string_to_bytes

logger = logging.getLogger()


class ClientManager(Manager):

    def update(self, client_id):
        updated = False
        for client in self.get():
            if client.client_id == client_id:
                updated = True
                client.timestamp = time.time()
        if not updated:
            logger.info('Add new client {}'.format(client_id))
            self.append(Client(client_id))
        self.save()


class Client(object):

    client_id = None
    timestamp = None

    def __init__(self, client_id):
        self.client_id = client_id
        self.timestamp = time.time()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.client_id == other.client_id
        else:
            return False

    def __hash__(self):
        return hash(self.client_id)

    def __bytes__(self):
        return string_to_bytes(self.__str__())

    def __str__(self):
        return '{{"client_id": "{}", "timestamp": {}}}'.format(self.client_id, self.timestamp)
