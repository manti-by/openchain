import logging

import tornado.ioloop
import tornado.web

from tracker.app.listener import Listener
from common.utils import init_logger

logger = logging.getLogger()


if __name__ == "__main__":
    init_logger()
    logger.info('Starting tracker application')

    app = tornado.web.Application([
        (r"/", Listener),
    ])
    app.listen(8112, address='192.168.112.10')

    logger.info('Listening for connections')
    tornado.ioloop.IOLoop.current().start()