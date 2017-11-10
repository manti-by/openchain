import json
import xxhash

from openchain.models.database import LevelDBAdapter
from openchain.models.factory import ModelFactory


class Manager:

    ns = None
    db = None

    queryset = []
    loaded = False

    def __init__(self):
        if self.db is None:
            self.ns = self.__class__.__name__.lower()
            self.db = LevelDBAdapter().connect(self.ns)

    def get(self) -> list:
        if not self.loaded:
            self.loaded = True
            for key, value in self.db.RangeIter():
                data = json.loads(value.decode())
                self.queryset.append(ModelFactory.get_model(self.ns)(**data))
        return self.queryset

    def set(self, qs: list, commit: bool=False):
        self.queryset = qs
        if commit:
            self.save()

    def delete(self, item: dict, commit: bool=False):
        for i in self.queryset:
            if i == item:
                del i
        if commit:
            self.save()

    def append(self, item: object, commit: bool=False):
        self.queryset.append(item)
        if commit:
            self.save()

    def save(self):
        batch = LevelDBAdapter.write_batch()
        for item in self.queryset:
            index = xxhash.xxh64()
            index.update(item.__bytes__)
            batch.Put(index.digest(), item.__bytes__)
        self.db.Write(batch, sync=True)


class Model:

    data = None
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
        self.objects.append(item=self, commit=True)
