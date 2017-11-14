import json
import xxhash

from openchain.adapters.plyvel import PlyvelAdapter
from openchain.models.factory import ModelFactory


class Manager:

    namespace = None
    db_adapter = PlyvelAdapter()

    queryset = None
    loaded = False

    def __init__(self):
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

    def set(self, qs: list, commit: bool=False):
        self.queryset = qs
        if commit:
            self.save()

    def delete(self, item: dict, commit: bool=False):
        if item in self.queryset:
            self.queryset.remove(item)
        if commit:
            self.save()

    def delete_all(self, commit: bool=False):
        self.queryset = []
        if commit:
            self.save()

    def append(self, item: object, commit: bool=False):
        if not self.loaded:
            self.load()
        self.queryset.append(item)
        if commit:
            self.save()

    def save(self):
        compact_list = []
        for item in self.queryset:
            index = xxhash.xxh64()
            index.update(item.__bytes__)
            compact_list.append({index.digest(): item.__bytes__})
        self.db_adapter.write_batch(self.namespace, compact_list)


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
