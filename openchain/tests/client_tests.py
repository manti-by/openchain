from openchain.models.factory import ModelFactory
from openchain.tests import BaseTestCase
from openchain.models.client import Client


class ClientModelTestCase(BaseTestCase):

    def setUp(self):
        Client.objects.delete_all()

    def test_client_creation(self):
        client = Client('client-01')
        client.save()

        self.assertIsInstance(client, Client)
        self.assertIsInstance(client.__dict__, dict)

        Client.objects.delete_all()

    def test_two_clients_creation(self):
        client_01 = Client('client-01')
        client_01.save()
        client_02 = Client('client-02')
        client_02.save()

        clients_count = len(Client.objects.get())
        self.assertEqual(clients_count, 2)

        Client.objects.delete_all()

    def test_client_update(self):
        client_01 = Client('client-01')
        client_01.save()
        client_02 = Client('client-02')
        client_02.save()
        client_02.client_id = 'client-03'
        client_02.save()

        clients_count = len(Client.objects.get())
        self.assertEqual(clients_count, 2)
        self.assertEqual(client_02.client_id, 'client-03')

        Client.objects.delete_all()

    def test_client_delete(self):
        client_01 = Client('client-01')
        client_01.save()
        client_02 = Client('client-02')
        client_02.save()
        Client.objects.delete(client_01)

        client_set = Client.objects.get()
        self.assertEqual(len(client_set), 1)
        self.assertEqual(client_set[0].client_id, 'client-02')

        Client.objects.delete_all()

    def test_client_set(self):
        Client.objects.set([Client('client-01'), Client('client-02')])

        clients_count = len(Client.objects.get())
        self.assertEqual(clients_count, 2)

        Client.objects.delete_all()

    def test_client_model_factory(self):
        client_model_instance = ModelFactory.get_model('client')
        self.assertEqual(client_model_instance, Client)
