from unittest import TestCase

from openchain.models.client import Client


class ClientTestCase(TestCase):

    def test_client_creation(self):
        client = Client('client-01')
        client.save()
        self.assertIsInstance(client, Client)
