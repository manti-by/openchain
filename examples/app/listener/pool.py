import json
import logging
import tornado.web

from openchain.models.client import Client

logger = logging.getLogger()


class PoolListener(tornado.web.RequestHandler):

    def get(self):
        logger.info('Processing get request')

        try:
            result = {
                'status': 200,
                'data': Client.objects.dict_list
            }
        except Exception as e:
            logger.error(e)
            result = {'status': 500, 'message': e}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result).encode())
        self.finish()

    def post(self):
        logger.info('Processing post request')

        try:
            client_id = self.request.headers.get('X-Client-Address', self.request.remote_ip)
            client = Client(client_id)
            client.save()
            result = {'status': 200, 'message': 'OK'}
        except Exception as e:
            logger.error(e)
            result = {'status': 500, 'message': e}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result).encode())
        self.finish()
