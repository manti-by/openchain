import logging

from tornado import web, ioloop

from .common.conf import settings
from .common.utils import init_logger
from .listener.pool import PoolListener

logger = logging.getLogger()


if __name__ == "__main__":

    init_logger(settings)
    logger.debug('Starting pool application')

    app = web.Application([
        (r"/", PoolListener),
    ])

    app.listen(settings['pool_server']['port'], address=settings['pool_server']['ip'])

    logger.debug('Listening for connections on {}:{}'.format(settings['pool_server']['ip'],
                                                             settings['pool_server']['port']))
    ioloop.IOLoop.current().start()
