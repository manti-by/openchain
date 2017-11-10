import json
import logging
import tornado.web

from openchain.models.logentry import LogEntry

logger = logging.getLogger()


class LoggerListener(tornado.web.RequestHandler):

    def get(self):
        logger.debug('[LOGGER] Processing get request')

        try:
            result = {
                'status': 200,
                'data': LogEntry.objects.get()
            }
        except Exception as e:
            logger.error(e)
            result = {'status': 500, 'message': e}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result).encode())
        self.finish()

    def post(self):
        logger.debug('[LOGGER] Processing post request')

        try:
            result = {'status': 204, 'message': 'No Content'}
            if self.request.body:
                log_entry = LogEntry(self.request.body)
                log_entry.save()
                result = {'status': 200, 'message': 'OK'}
        except Exception as e:
            logger.error(e)
            result = {'status': 500, 'message': e}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result).encode())
        self.finish()
