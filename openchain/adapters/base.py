import os


class Singleton(type):

    instance_set = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instance_set:
            cls.instance_set[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance_set[cls]


class BaseAdapter(metaclass=Singleton):

    db_path = os.getenv('DATABASE_PATH', '/var/lib/openchain/')
    connection_set = {}

    def connect(self, namespace: str):
        raise NotImplementedError

    def get(self, namespace: str, key: bytes) -> bytes:
        raise NotImplementedError

    def put(self, namespace, key: bytes, value: bytes):
        raise NotImplementedError

    def delete(self, namespace: str, key: bytes) -> bytes:
        raise NotImplementedError

    def iterator(self, namespace: str) -> callable:
        raise NotImplementedError

    def batch_put(self, namespace: str, item_list: list) -> callable:
        raise NotImplementedError

    def batch_delete(self, namespace: str, item_list: list) -> callable:
        raise NotImplementedError
