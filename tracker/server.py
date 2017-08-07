import logging

import tornado.ioloop
import tornado.web

from tracker.app.listener import Listener
from common.utils import init_logger

logger = logging.getLogger()


def make_app():
    return tornado.web.Application([
        (r"/", Listener),
    ])


if __name__ == "__main__":
    init_logger()
    logger.info('Starting tracker application')

    app = make_app()
    app.listen(8112)

    logger.info('Listening for connections')
    tornado.ioloop.IOLoop.current().start()