import json
import logging
import tornado.web

from common.conf import settings

logger = logging.getLogger()


class BuilderListener(tornado.web.RequestHandler):

    def get(self):
        logger.info('Processing get request')
        try:
            file = open(settings['builder_tree_path'], 'r')
            result = {
                'status': 200,
                'blockchain': file.read()
            }
        except Exception as e:
            logger.error(e)
            result = {'status': 500, 'message': e}

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result).encode())
        self.finish()
