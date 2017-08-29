import time

from hashlib import sha256

from common.models import Manager
from common.utils import string_to_bytes


class BlockManager(Manager):

    def append(self, item):
        pass


class Block(object):

    data = None
    hash = None
    prev = None
    timestamp = None

    def __init__(self, data, prev):
        self.data = data
        self.prev = prev
        self.timestamp = time.time()
        self.hash = sha256({'prev': self.prev, 'data': self.data, 'timestamp': self.timestamp})

    def __bytes__(self):
        return string_to_bytes(self.__str__())

    def __str__(self):
        return '{{"hash": {},"prev": {}, "data": "{}", "timestamp": {}}}'.format(self.hash, self.prev,
                                                                                 self.data, self.timestamp)

    def __next__(self, data):
        return Block(data, self.hash)