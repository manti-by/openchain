import json
import xxhash

from openchain.adapters.plyvel import PlyvelAdapter
from openchain.models.factory import ModelFactory


class Manager:

    db_adapter = PlyvelAdapter()

    def __init__(self):
        self.loaded = False
        self.queryset = []
        self.namespace = self.__class__.__name__.lower()
        if self.namespace != 'manager':
            self.namespace = self.namespace.replace('manager', '')
        self.db_adapter.connect(self.namespace)

    def load(self, force_load=False):
        if not self.loaded or force_load:
            self.queryset = []
            for key, value in self.db_adapter.iterator(self.namespace):
                data = json.loads(value.decode())
                self.queryset.append(ModelFactory.get_model(self.namespace)(**data))
            self.loaded = True

    def get(self) -> list:
        self.load()
        return self.queryset

    def set(self, qs: list):
        self.delete_all()
        self.queryset = qs
        self.save()

    def search(self, search_item):
        self.load()
        for item in self.queryset:
            if search_item == item:
                return item

    def append(self, item: object, commit: bool=False):
        self.load()
        self.queryset.append(item)
        if commit:
            self.save()

    def delete(self, item: object):
        if item in self.queryset:
            self.queryset.remove(item)
            index = next(iter(item.__dict__)).encode()
            self.db_adapter.delete(self.namespace, index)

    def delete_list(self, item_list: list):
        hashed_list = []
        for item in item_list:
            index = xxhash.xxh64()
            index.update(item.__bytes__)
            hashed_list.append({index.digest(): item.__bytes__})

        self.db_adapter.batch_delete(self.namespace, hashed_list)
        self.load(True)

    def delete_all(self):
        self.load()
        self.db_adapter.batch_delete(self.namespace, self.hashed_list)
        self.queryset = []

    def save(self):
        self.db_adapter.batch_put(self.namespace, self.hashed_list)

    @property
    def hashed_list(self):
        result = []
        if self.queryset:
            for item in self.queryset:
                index = xxhash.xxh64()
                index.update(item.__bytes__)
                result.append({index.digest(): item.__bytes__})
        return result

    @property
    def dict_list(self):
        result = []
        for item in self.queryset:
            result.append(item.__dict__)
        return result


class Model:

    objects = Manager()

    @property
    def __dict__(self) -> dict:
        raise NotImplementedError()

    @property
    def __str__(self) -> str:
        return json.dumps(self.__dict__)

    @property
    def __bytes__(self) -> bytes:
        return self.__str__.encode()

    def save(self):
        self.objects.append(self, True)
