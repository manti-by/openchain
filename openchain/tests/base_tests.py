from openchain.models.base import Model
from openchain.models.factory import ModelFactory
from openchain.tests import BaseTestCase
from openchain.adapters.base import BaseAdapter
from openchain.adapters.plyvel import PlyvelAdapter


class ModelTestCase(BaseTestCase):

    def test_model(self):
        model = Model()
        with self.assertRaises(NotImplementedError):
            print(model.__dict__)

    def test_model_factory(self):
        logentry_model_instance = ModelFactory.get_model('not_existing_model')
        self.assertIsNone(logentry_model_instance)


class AdapterTestCase(BaseTestCase):

    def setUp(self):
        self.test_key = b'key'
        self.test_value = b'value'
        self.namespace = 'test'

    def test_base_crud(self):
        adapter = BaseAdapter()

        with self.assertRaises(NotImplementedError):
            adapter.connect(self.namespace)

        with self.assertRaises(NotImplementedError):
            adapter.put(self.namespace, self.test_key, self.test_value)

        with self.assertRaises(NotImplementedError):
            adapter.get(self.namespace, self.test_key)

        with self.assertRaises(NotImplementedError):
            adapter.delete(self.namespace, self.test_key)

        with self.assertRaises(NotImplementedError):
            adapter.iterator(self.namespace)

        with self.assertRaises(NotImplementedError):
            adapter.write_batch(self.namespace, [])

    def test_plyvel_crud(self):
        adapter = PlyvelAdapter()
        adapter.connect(self.namespace)

        adapter.put(self.namespace, self.test_key, self.test_value)
        read_value = adapter.get(self.namespace, self.test_key)

        adapter.delete(self.namespace, self.test_key)
        delete_value = adapter.get(self.namespace, self.test_key)

        self.assertEqual(read_value, self.test_value)
        self.assertIsNone(delete_value)
