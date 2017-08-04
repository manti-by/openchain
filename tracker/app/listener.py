
import leveldb
import tornado.web

from app.models import ClientManager
from app.utils import get_client_id


class Listener(tornado.web.RequestHandler):

    clients_key = b'clients'

    def initialize(self):
        self.db = leveldb.LevelDB('./db')
        try:
            self.db.Get(self.clients_key)
        except:
            self.db.Put(self.clients_key, b'[]')

    def update_clients(self):
        clients = ClientManager(self.db.Get(self.clients_key))
        clients.update_client(get_client_id(self.request))
        self.db.Put(self.clients_key, clients.__bytes__())
        return clients

    def get(self):
        clients = self.update_clients()
        self.set_header('Content-Type', 'application/json')
        self.write(clients.__bytes__())
        self.finish()
