from openchain.tests import BaseTestCase
from openchain.models.client import Client


class ClientTestCase(BaseTestCase):

    def test_client_creation(self):
        client = Client('client-01')
        client.save()
        self.assertIsInstance(client, Client)

    def test_client_set(self):
        Client.objects.delete_all(commit=True)
        client = Client('client-02')
        client.save()
        client = Client('client-03')
        client.save()
        clients_count = len(client.objects.get())
        self.assertEqual(clients_count, 2)
