import logging

import tornado.ioloop
import tornado.web

from examples.common.conf import settings
from examples.common.utils import init_logger
from examples.listener.logger import LoggerListener

logger = logging.getLogger()


if __name__ == "__main__":
    init_logger(settings)
    logger.debug('[LOGGER] Starting logger application')

    app = tornado.web.Application([
        (r"/", LoggerListener),
    ])

    app.listen(settings['log_server']['port'], address=settings['log_server']['ip'])

    logger.debug('[LOGGER] Listening for connections on {}:{}'.format(settings['log_server']['ip'],
                                                                      settings['log_server']['port']))
    tornado.ioloop.IOLoop.current().start()
