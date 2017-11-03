from unittest import TestCase
from open_blockchain.models.base import Model


class BaseTestCase(TestCase):

    def test_model(self):
        m = Model
        self.assertEqual(m.__class__, 'Model')
