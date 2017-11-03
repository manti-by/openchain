import json
import leveldb


class Manager:

    qs = []

    def get(self) -> list:
        return self.qs

    def set(self, qs: list, commit: bool=False):
        self.qs = qs
        if commit:
            self.save()

    def append(self, item: object):
        self.qs.append(item)

    def save(self):
        db = leveldb.LevelDB('./db/{}'.format(self.__name__.lower()))
        batch = leveldb.WriteBatch()
        for i in self.qs:
            db.Put(i.pk.encode(), i)
        db.Write(batch, sync=True)


class Model:

    objects = Manager()

    def __bytes__(self):
        return self.__str__().encode()

    def __str__(self):
        raise json.dumps(self.__dict__())

    def __dict__(self):
        raise NotImplementedError

    @property
    def pk(self):
        raise NotImplementedError

    def save(self):
        self.objects.append(self)
        self.objects.save()
