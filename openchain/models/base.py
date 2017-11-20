import json
import xxhash

from openchain.adapters.plyvel import PlyvelAdapter
from openchain.models.factory import ModelFactory


class Manager:

    db_adapter = PlyvelAdapter()

    def __init__(self):
        self.loaded = False
        self.queryset = None
        self.namespace = self.__class__.__name__.lower()
        if self.namespace != 'manager':
            self.namespace = self.namespace.replace('manager', '')
        self.db_adapter.connect(self.namespace)

    def load(self):
        if not self.loaded:
            self.queryset = []
            for key, value in self.db_adapter.iterator(self.namespace):
                data = json.loads(value.decode())
                self.queryset.append(ModelFactory.get_model(self.namespace)(**data))
            self.loaded = True

    def get(self) -> list:
        if not self.loaded:
            self.load()
        return self.queryset

    def set(self, qs: list):
        self.delete_all()
        self.queryset = qs
        self.save()

    def search(self, search_item):
        if not self.loaded:
            self.load()
        for item in self.queryset:
            if search_item == item:
                return item

    def append(self, item: object, commit: bool=False):
        if not self.loaded:
            self.load()
        self.queryset.append(item)
        if commit:
            self.save()

    def delete(self, item: object):
        if item in self.queryset:
            self.queryset.remove(item)
            index = next(iter(item.__dict__)).encode()
            self.db_adapter.delete(self.namespace, index)

    def delete_all(self):
        if not self.loaded:
            self.load()
        self.db_adapter.batch_delete(self.namespace, self.compact_list)
        self.queryset = []

    def save(self):
        self.db_adapter.batch_put(self.namespace, self.compact_list)

    @property
    def compact_list(self):
        if self.queryset:
            for item in self.queryset:
                index = xxhash.xxh64()
                index.update(item.__bytes__)
                yield {index.digest(): item.__bytes__}


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
