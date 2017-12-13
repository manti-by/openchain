import json
import logging
import tornado.web

from openchain.models.block import Block
from openchain.models.transaction import Transaction

logger = logging.getLogger()


class MinerListener(tornado.web.RequestHandler):

    def get(self):
        logger.debug('[MINER] Processing get request')

        try:
            result = {
                'status': 200,
                'data': Block.objects.blockchain.__dict__
            }
        except Exception as e:
            logger.error('[MINER] {}'.format(e))
            result = {'status': 500, 'message': e}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result).encode())
        self.finish()

    def post(self):
        logger.debug('[MINER] Processing post request')

        try:
            result = {'status': 204, 'message': 'No Content'}
            if self.request.body:
                transaction = json.loads(self.request.body.decode('utf-8'))
                transaction = Transaction(**transaction)
                transaction.save()
                result = {'status': 200, 'message': 'OK'}
        except Exception as e:
            logger.error('[MINER] {}'.format(e))
            result = {'status': 500, 'message': e}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result).encode())
        self.finish()
