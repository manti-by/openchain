import leveldb
import logging

from common.utils import string_to_bytes

logger = logging.getLogger()


class Manager(object):

    _data = []

    def __init__(self):
        self.db = leveldb.LevelDB('./db')
        try:
            self._data = self.db.Get(self.__class__)
        except:
            logger.info('Initialize DB for {}'.format(self.__class__))
            self.db.Put(self.__class__, b'[]')

    def __bytes__(self):
        return string_to_bytes(self.__str__())

    def __str__(self):
        return '[%s]' % ', '.join([c.__str__() for c in self._data])

    def get(self):
        return self._data

    def set(self, data):
        self._data = data

    def append(self, item):
        self._data.append(item)

    def save(self):
        self.db.Put(self.__class__, self.__bytes__)