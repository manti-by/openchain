import logging
import tornado.web

from openchain.models.client import Client

logger = logging.getLogger()


class PoolListener(tornado.web.RequestHandler):

    def get(self):
        logger.debug('[POOL] Processing get request')

        try:
            client_id = self.request.headers.get('X-Client-STUN-Address', self.request.remote_ip)
            client = Client(client_id)
            client.save()
            data = client.objects.get()
        except Exception as e:
            logger.error('[POOL] {}'.format(e))
            data = e

        self.set_header('Content-Type', 'application/json')
        self.write(data.__bytes__())
        self.finish()
