import logging
import leveldb
import tornado.web

from tracker.app.models import ClientManager
from common.utils import get_client_id

logger = logging.getLogger()


class Listener(tornado.web.RequestHandler):

    clients_key = b'clients'

    def initialize(self):
        self.db = leveldb.LevelDB('./db')
        try:
            self.db.Get(self.clients_key)
        except:
            logger.info('Initialize clients DB')
            self.db.Put(self.clients_key, b'[]')

    def update_clients(self):
        try:
            clients = ClientManager(self.db.Get(self.clients_key))
            clients.update_client(get_client_id(self.request))
            self.db.Put(self.clients_key, clients.__bytes__())
            return clients
        except Exception as e:
            logger.error(e)

    def get(self):
        logger.info('Processing get request')
        clients = self.update_clients()
        self.set_header('Content-Type', 'application/json')
        self.write(clients.__bytes__())
        self.finish()
