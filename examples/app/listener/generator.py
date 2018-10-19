import json
import logging
import tornado.web

from openchain.models.transaction import Transaction

logger = logging.getLogger()


class GeneratorListener(tornado.web.RequestHandler):

    def post(self):
        logger.info('Processing post request')

        try:
            result = {'status': 204, 'message': 'No Content'}
            if self.request.body:
                transaction = json.loads(self.request.body.decode('utf-8'))
                transaction = Transaction(**transaction)
                transaction.save()
                result = {'status': 200, 'message': 'OK'}
        except Exception as e:
            logger.error(e)
            result = {'status': 500, 'message': e}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result).encode())
        self.finish()
