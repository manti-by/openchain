import time
import logging

from openchain.models.base import Model, Manager

logger = logging.getLogger()


class ClientManager(Manager):

    def update(self, client_id):
        updated = False
        for client in self.get():
            if client.client_id == client_id:
                updated = True
                client.timestamp = time.time()
        if not updated:
            logger.debug('Add new client {}'.format(client_id))
            self.append(Client(client_id))
        self.save()


class Client(Model):

    client_id = None
    timestamp = None

    objects = ClientManager()

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

    def __dict__(self):
        return {
            'client_id': self.client_id,
            'timestamp': self.timestamp
        }
