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

    def write_batch(self, namespace, item_list):
        with self.connection_set[namespace].write_batch() as batch:
            for item  in item_list:
                for key, value in item.items():
                    batch.put(key, value)

    @staticmethod
    def drop_all_and_close_connection(accidental_protection_token):
        if accidental_protection_token != b'Accidental protection token':
            return
        for namespace, connection in PlyvelAdapter.connection_set.items():
            connection.close()
            filename = os.path.join(PlyvelAdapter.db_path, namespace)
            plyvel.destroy_db(filename)
        PlyvelAdapter.connection_set = {}
