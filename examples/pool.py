import logging

import tornado.ioloop
import tornado.web

from examples.common.conf import settings
from examples.common.utils import init_logger
from examples.listener.pool import PoolListener

logger = logging.getLogger()


if __name__ == "__main__":
    init_logger(settings)
    logger.debug('[POOL] Starting pool application')

    app = tornado.web.Application([
        (r"/", PoolListener),
    ])

    app.listen(settings['pool_server']['port'], address=settings['pool_server']['ip'])

    logger.debug('[POOL] Listening for connections on {}:{}'.format(settings['pool_server']['ip'],
                                                                    settings['pool_server']['port']))
    tornado.ioloop.IOLoop.current().start()
