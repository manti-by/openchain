import os
import leveldb


class Singleton(type):

    instance_set = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instance_set:
            cls.instance_set[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance_set[cls]


class LevelDBAdapter(metaclass=Singleton):

    cs = {}

    def connect(self, namespace):
        db_path = os.getenv('DATABASE_PATH', '/var/tmp/leveldb/')
        if namespace not in self.cs:
            filename = os.path.join(db_path, namespace)
            self.cs[namespace] = leveldb.LevelDB(filename)
        return self.cs[namespace]

    @staticmethod
    def write_batch():
        return leveldb.WriteBatch()
