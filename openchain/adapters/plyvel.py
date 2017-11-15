import os
import plyvel

from openchain.adapters.base import BaseAdapter


class PlyvelAdapter(BaseAdapter):

    def connect(self, namespace):
        if namespace not in self.connection_set:
            filename = os.path.join(self.db_path, namespace)
            self.connection_set[namespace] = plyvel.DB(filename, create_if_missing=True)

    def get(self, namespace, key):
        return self.connection_set[namespace].get(key)

    def put(self, namespace, key, value):
        self.connection_set[namespace].put(key, value)

    def delete(self, namespace, key):
        self.connection_set[namespace].delete(key)

    def iterator(self, namespace):
        return self.connection_set[namespace].iterator()

    def batch_put(self, namespace, item_list):
        with self.connection_set[namespace].write_batch() as batch:
            for item in item_list:
                for key, value in item.items():
                    batch.put(key, value)
            batch.write()

    def batch_delete(self, namespace, item_list):
        with self.connection_set[namespace].write_batch() as batch:
            for item in item_list:
                batch.delete(next(iter(item)))
            batch.write()
