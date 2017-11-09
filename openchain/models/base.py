import os
import json
import leveldb
import xxhash


class Manager:

    db = None
    qs = []

    def __init__(self):
        db_path = os.getenv('DATABASE_PATH', '/var/tmp/leveldb/')
        filename = os.path.join(db_path, self.__class__.__name__.lower())
        self.db = leveldb.LevelDB(filename)
        for key, value in self.db.RangeIter():
            data = json.loads(value.decode())
            self.append(self.model_from_dict(data))

    def get(self) -> list:
        return self.qs

    def set(self, qs: list, commit: bool=False):
        self.qs = qs
        if commit:
            self.save()

    def delete(self, item: dict, commit: bool=False):
        for i in self.qs:
            if i == item:
                del i
        if commit:
            self.save()

    def append(self, item: object, commit: bool=False):
        self.qs.append(item)
        if commit:
            self.save()

    def save(self):
        batch = leveldb.WriteBatch()
        for item in self.qs:
            index = xxhash.xxh64()
            index.update(item.__bytes__)
            self.db.Put(index.digest(), item.__bytes__)
        self.db.Write(batch, sync=True)

    def model_from_dict(self, data):
        raise NotImplementedError


class Model:

    data = None
    objects = Manager
    manager = None

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
        if self.manager is None:
            self.manager = self.objects()
        self.manager.append(self, commit=True)
