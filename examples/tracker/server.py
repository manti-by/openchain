import logging

import tornado.web
import tornado.ioloop

from .listener import Listener
from open_blockchain.utils import init_logger

logger = logging.getLogger()


if __name__ == "__main__":
    local = True

    init_logger()
    logger.info('Starting tracker application')

    app = tornado.web.Application([
        (r"/", Listener),
    ])

    server_ip = '192.168.112.10'
    if local:
        server_ip = '127.0.0.1'

    app.listen(8112, address=server_ip)

    logger.info('Listening for connections on {}:{}'.format(server_ip, 8112))
    tornado.ioloop.IOLoop.current().start()
