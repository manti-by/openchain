import json
import logging

import tornado.ioloop
import tornado.web

from common.conf import settings
from common.utils import init_logger
from listener.builder import BuilderListener

from openchain.models.block import Block
from openchain.models.factory import BlockchainFactory

logger = logging.getLogger()


def build_tree():
    logger.info('Start blockchain tree builder')

    try:
        block_list = Block.objects.get()
        logger.debug('Block list count {}'.format(len(block_list)))

        block_chain = BlockchainFactory.build_blockchain(block_list)
        logger.debug('Last block hash {}'.format(block_chain.last_block_hash))

        file = open(settings['builder_tree_path'], 'w')
        file.write(json.dumps(block_chain.__dict__))

        logger.info('Finished blockchain tree building')
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    init_logger(settings)
    logger.info('Starting the application')

    app = tornado.web.Application([
        (r"/", BuilderListener),
    ])
    app.listen(settings['builder_server']['port'])

    io_loop = tornado.ioloop.IOLoop.current()
    scheduler = tornado.ioloop.PeriodicCallback(build_tree, 60000)

    logger.info('Listening for connections on {}:{}'.format(settings['miner_server']['ip'],
                                                            settings['miner_server']['port']))
    scheduler.start()
    io_loop.start()
