import json
import leveldb
import logging

from open_blockchain.utils import string_to_bytes

logger = logging.getLogger()


class Manager(object):

    query_set = []

    def __init__(self):
        self.db = leveldb.LevelDB('./db')
        try:
            self._data = self.db.Get(self.__class__)
        except Exception:
            logger.debug('Initialize DB for {}'.format(self.__class__))
            self.db.Put(self.__class__, b'[]')

    def __bytes__(self):
        return string_to_bytes(self.__str__())

    def __str__(self):
        return '[%s]' % ', '.join([i.__str__() for i in self.query_set])

    def get(self):
        return self.query_set

    def set(self, query_set):
        self.query_set = query_set

    def append(self, item):
        self.query_set.append(item)

    def save(self):
        self.db.Put(self.__class__, self.__bytes__)


class Model:

    objects = Manager()

    def __bytes__(self):
        return string_to_bytes(self.__str__())

    def __str__(self):
        raise json.dumps(self.__dict__())

    def __dict__(self):
        raise NotImplementedError

    def save(self):
        self.objects.append(self)
        self.objects.save()
