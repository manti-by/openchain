import logging

from tornado import web, ioloop

from .common.conf import settings
from .common.utils import init_logger
from .listener.traker import TrackerListener

logger = logging.getLogger()


if __name__ == "__main__":
    local = True

    init_logger(settings)
    logger.debug('Starting tracker application')

    app = web.Application([
        (r"/", TrackerListener),
    ])

    server_ip = '192.168.112.10'
    if local:
        server_ip = '127.0.0.1'

    app.listen(8112, address=server_ip)

    logger.debug('Listening for connections on {}:{}'.format(server_ip, 8112))
    ioloop.IOLoop.current().start()
