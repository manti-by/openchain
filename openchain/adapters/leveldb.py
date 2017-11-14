import os
import leveldb

from openchain.adapters.base import BaseAdapter


class LevelDBAdapter(BaseAdapter):

    def connect(self, namespace):
        if namespace not in self.connection_set:
            filename = os.path.join(self.db_path, namespace)
            self.connection_set[namespace] = leveldb.LevelDB(filename, create_if_missing=False)

    def get(self, namespace, key):
        return self.connection_set[namespace].Get(key)

    def put(self, namespace, key, value):
        self.connection_set[namespace].Put(key, value)

    def delete(self, namespace, key):
        self.connection_set[namespace].Delete(key)

    def iterator(self, namespace):
        return self.connection_set[namespace].RangeIter()

    def write_batch(self, namespace, items):
        with self.connection_set[namespace].WriteBatch() as batch:
            for key, value in [i.items() for i in items]:
                batch.Put(key, value)
            self.connection_set[namespace].Write(batch)

    @staticmethod
    def drop_all_and_close_connection(accidental_protection_token):
        if accidental_protection_token != b'Accidental protection token':
            return
        for namespace, connection in LevelDBAdapter.connection_set.items():
            filename = os.path.join(LevelDBAdapter.db_path, namespace)
            leveldb.DestroyDB(filename)
            del LevelDBAdapter.connection_set[namespace]
